import json
import logging
import os
from datetime import datetime

from rest_framework.views import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from django.conf import settings

from .models import Testcases
from .serializers import TestcasesModelSerializer, TestcasesRunModelSerializer
from interfaces.models import Interfaces
from envs.models import Envs

from utils import data_handle, common
logger = logging.getLogger('mytest')


class TestcasesViewSet(viewsets.ModelViewSet):
	queryset = Testcases.objects.all()
	serializer_class = TestcasesModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['create_time']

	def retrieve(self, request, *args, **kwargs):
		testcase_obj = self.get_object()
		request_include = json.loads(testcase_obj.include, encoding='utf-8')
		test_data = json.loads(testcase_obj.request, encoding='utf-8')['test']

		data = {
			'author': testcase_obj.author,
			'testcase_name': testcase_obj.name,
			'url': test_data['request']['url'],
			'method': test_data['request']['method'],
			'jsonVariable': json.dumps(test_data['request'].get('json'), ensure_ascii=False),
			'selected_interface_id': testcase_obj.interface_id,
			'selected_project_id': Interfaces.objects.get(id=testcase_obj.interface_id).project_id,
			'selected_configure_id': request_include['config'],
			'selected_testcase_id': request_include['testcases'],
			'parameterized': data_handle.key_value(test_data.get('parameters')),
			'extract': data_handle.key_value(test_data.get('extract')),
			'setupHooks': data_handle.key_(test_data.get('setup_hooks')),
			'teardownHooks': data_handle.key_(test_data.get('teardown_hooks')),
			'globalVar': data_handle.key_value_paramtype(test_data.get('variables')),
			'validate': data_handle.handle_validate(test_data.get('validate')),
			'header': data_handle.key_value(test_data.get('request').get('headers')),
			'param': data_handle.key_value(test_data.get('request').get('params')),
			'variable': data_handle.key_value_paramtype(test_data['request'].get('data'))
		}

		return Response(data)

	@action(methods=['post'], detail=True)
	def run(self, request, *args, **kwargs):
		"""
		取出用例数据并构造参数 --> 生成yaml文件 --> 运行用例 --> 生成报告
		"""
		instance = self.get_object()
		response = super().create(request, *args, **kwargs)
		env_id = response.data.serializer.validated_data.get('env_id')
		testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
		os.mkdir(testcase_dir_path)
		env = Envs.objects.filter(id=env_id).first()
		# 生成ymal文件
		common.generate_testcase_file(instance, env, testcase_dir_path)
		return common.run_testcase(instance, testcase_dir_path)

	def get_serializer_class(self):
		return TestcasesRunModelSerializer if self.action == 'run' else self.serializer_class

	def perform_create(self, serializer):
		if self.action == 'run':
			pass
		else:
			serializer.save()
