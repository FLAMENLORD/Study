import logging
import os
from datetime import datetime

from django.db.models import Count
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework.decorators import action
from rest_framework import permissions

from . import serializers
from utils import common
from utils.pagination import MyPagination
from utils.filters import LimitFilter
from django.conf import settings
from .models import Projects
from interfaces.models import Interfaces
from testsuits.models import Testsuits
from testcases.models import Testcases
from envs.models import Envs

logger = logging.getLogger('mytest')


class ProjectsViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id', 'programmer', 'tester']
	ordering_fields = ['id']
	pagination_class = MyPagination

	queryset = Projects.objects.all()
	serializer_class = serializers.ProjectsModelSerializer

	def list(self, request, *args, **kwargs):
		response = super().list(request, *args, **kwargs)
		data = response.data.get('results')

		if data:
			for project_data in data:
				project_id = project_data.get('id')
				# 项目接口总数
				project_data['interfaces'] = Interfaces.objects.filter(project_id=project_id).count()
				# 项目套件总数
				project_data['testsuits'] = Testsuits.objects.filter(project_id=project_id).count()

				# 项目下接口的用例总数
				interfaces_qs = Interfaces.objects.filter(project_id=project_id)
				testcases_query_set = interfaces_qs.values('id').annotate(testcases_count=Count('testcases'))
				project_data['testcases'] = sum([i.get('testcases_count') for i in testcases_query_set])

				# 项目下的配置总数
				configures_query_set = interfaces_qs.values('id').annotate(configures_count=Count('configures'))
				project_data['configures'] = sum([i.get('configures_count') for i in configures_query_set])

		res = {
			"data": data,
			"total": response.data['count'],
			"statusCode": response.status_code
		}
		return Response(res)

	# 查询项目名称列表
	@action(methods=['get'], detail=False)
	def names(self, request, *args, **kwargs):
		qs = self.get_queryset()
		return Response(self.get_serializer(qs, many=True).data)

	# 查询项目下的接口信息
	@action(detail=True)
	def interfaces(self, request, *args, **kwargs):
		response = self.retrieve(request, *args, **kwargs)
		return Response(response.data['interfaces'])

	@action(methods=['post'], detail=True)
	def run(self, request, *args, **kwargs):
		"""
		根据接口，取出所有用例数据 --> 生成yaml文件 --> 运行用例 --> 生成报告
		"""
		instance = self.get_object()
		response = super().create(request, *args, **kwargs)
		env_id = response.data.serializer.validated_data.get('env_id')
		testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%filter(id=1)S%f'))
		os.mkdir(testcase_dir_path)

		env = Envs.objects.filter(id=env_id).first()
		interface_qs = Interfaces.objects.filter(project=instance)
		if not interface_qs.exists():
			data = {
				'result': False,
				'message': '此项目下无接口，无法运行'
			}
			return Response(data, status=400)

		runnable_testcase_obj = []
		for interface_obj in interface_qs:
			# 接口下的所有用例
			testcase_qs = Testcases.objects.filter(interface=interface_obj)

			# 判断是否存在用例，若存在，则合并列表
			if testcase_qs.exists():
				runnable_testcase_obj.extend(list(testcase_qs))

		if len(runnable_testcase_obj) == 0:
			data = {
				'result': False,
				'message': '此项目下无用例，无法运行'
			}
			return Response(data, status=400)

		for testcase_obj in runnable_testcase_obj:
			common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

		return common.run_testcase(instance, testcase_dir_path)

	def get_serializer_class(self):
		if self.action == 'names':
			return serializers.ProjectsNamesModelSerializer
		if self.action == 'interfaces':
			return serializers.InterfacesByProjectIdModelSerializer
		if self.action == 'run':
			return serializers.ProjectsRunModelSerializer
		else:
			return self.serializer_class

	def perform_create(self, serializer):
		if self.action == 'run':
			pass
		else:
			serializer.save()



