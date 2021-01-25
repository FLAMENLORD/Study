import logging
import re
import os
from datetime import datetime


from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import Response
from rest_framework.decorators import action
from rest_framework import serializers

from django.conf import settings
from .models import Testsuits
from interfaces.models import Interfaces
from envs.models import Envs
from testcases.models import Testcases
from .serializers import TestsuitsModelSerializer, TestsuitsRunModelSerializer
from utils import common

logger = logging.getLogger('mytest')


def validate_include(value):
	obj = re.match(r'^\[\d+(,\d+)*\]$', value)
	if obj is None:
		raise serializers.ValidationError('参数格式错误')
	else:
		res = obj.group()
		try:
			for i in eval(res):
				if not Interfaces.objects.filter(id=i).exists():
					raise serializers.ValidationError(f'接口id【{i}】不存在')
		except:
			raise serializers.ValidationError('参数格式错误')


class TestsuitsViewSet(viewsets.ModelViewSet):
	queryset = Testsuits.objects.all()
	serializer_class = TestsuitsModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['id', 'name', 'create_time']

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		data = {
			'name': instance.name,
			'project_id': instance.project_id,
			'include': instance.include
		}
		return Response(data)

	@action(methods=['post'], detail=True)
	def run(self, request, *args, **kwargs):
		instance = self.get_object()
		response = super().create(request, *args, **kwargs)
		env_id = response.data.serializer.validated_data.get('env_id')
		testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
		os.mkdir(testcase_dir_path)

		env = Envs.objects.filter(id=env_id).first()

		if len(instance.include) == 0:
			data = {
				'result': False,
				'message': '此套件下无接口，无法运行'
			}
			return Response(data, status=400)

		# 获取套件包含的接口
		interface_obj_list = []
		for interface_id in eval(instance.include):
			interface_obj = Interfaces.objects.filter(id=interface_id)[0]
			interface_obj_list.append(interface_obj)

		runnable_testcase_obj = []
		for interface_obj in interface_obj_list:
			# 接口下的所有用例
			testcase_qs = Testcases.objects.filter(interface=interface_obj)

			# 判断是否存在用例，若存在，则合并列表
			if testcase_qs.exists():
				runnable_testcase_obj.extend(list(testcase_qs))

		if len(runnable_testcase_obj) == 0:
			data = {
				'result': False,
				'message': '此套件下无用例，无法运行'
			}
			return Response(data, status=400)

		for testcase_obj in runnable_testcase_obj:
			common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

		return common.run_testcase(instance, testcase_dir_path)

	def get_serializer_class(self):
		return TestsuitsRunModelSerializer if self.action == 'run' else self.serializer_class

	def perform_create(self, serializer):
		if self.action == 'run':
			pass
		else:
			serializer.save()
