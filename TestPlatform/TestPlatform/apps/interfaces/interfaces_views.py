import logging
import os
from datetime import datetime

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework import permissions
from rest_framework.decorators import action

from utils import common
from django.conf import settings
from . import serializers
from .models import Interfaces
from testcases.models import Testcases
from configures.models import Configures
from envs.models import Envs

logger = logging.getLogger('mytest')


class InterfacesViewSet(viewsets.ModelViewSet):
	queryset = Interfaces.objects.all()
	serializer_class = serializers.InterfacesModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['id', 'name', 'create_time']

	def list(self, request, *args, **kwargs):
		response = super().list(request, *args, **kwargs)
		results = response.data['results']
		for interface_data in results:
			interface_id = interface_data.get('id')
			# 接口用例总数
			interface_data['testcases'] = Testcases.objects.filter(interface_id=interface_id).count()
			# 接口配置总数
			interface_data['configures'] = Configures.objects.filter(interface_id=interface_id).count()
		return response

	@action(detail=True)
	def project(self, request, *args, **kwargs):
		interface_obj = self.get_object()
		serializer_obj = self.get_serializer(instance=interface_obj)
		return Response(serializer_obj.data)

	@action(detail=True)
	def testcases(self, request, *args, **kwargs):
		response = self.retrieve(request, *args, **kwargs)
		response.data = response.data['testcases']
		return response

	@action(methods=['get'], detail=True)
	def configs(self, request, *args, **kwargs):
		response = self.retrieve(request, *args, **kwargs)
		response.data = response.data['configures']
		return response

	@action(methods=['post'], detail=True)
	def run(self, request, *args, **kwargs):
		instance = self.get_object()
		response = super().create(request, *args, **kwargs)
		env_id = response.data.serializer.validated_data.get('env_id')
		testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%filter(id=1)S%f'))
		os.mkdir(testcase_dir_path)

		env = Envs.objects.filter(id=env_id).first()
		testcase_qs = Testcases.objects.filter(interface=instance)
		if not testcase_qs.exists():
			data = {
				'result': False,
				'message': '此接口下无用例，无法运行'
			}
			return Response(data, status=400)

		for testcase_obj in testcase_qs:
			common.generate_testcase_file(testcase_obj, env, testcase_dir_path)

		return common.run_testcase(instance, testcase_dir_path)

	def get_serializer_class(self):
		if self.action == 'project':
			return serializers.ProjectByInterfaceIdModelSerializer
		if self.action == 'testcases':
			return serializers.TestcasesByInterfaceIdModelSerializer
		if self.action == 'configs':
			return serializers.ConfiguresByInterfaceIdModelSerializer
		if self.action == 'run':
			return serializers.InterfacesRunModelSerializer
		else:
			return self.serializer_class

	def perform_create(self, serializer):
		if self.action == 'run':
			pass
		else:
			serializer.save()
