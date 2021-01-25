from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils import common
from .models import Projects
from interfaces.models import Interfaces
from testcases.models import Testcases
from testsuits.models import Testsuits
from debugtalks.models import DebugTalks
from utils import validates


# 接口模型序列化器类
class InterfacesNamesModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Interfaces
		fields = ('id', 'name')


class ProjectsNamesModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Projects
		fields = ('id', 'name')


class ProjectsModelSerializer(serializers.ModelSerializer):
	def validate_name(self, value):
		if 'test' in value:
			raise serializers.ValidationError("接口名称中不能包含'test'")
		return value

	class Meta:
		model = Projects
		exclude = ('update_time', )

		extra_kwargs = {
			'name': {
				'label': '项目名',
				'help_text': '项目名',
				'max_length': 200,
				'error_messages': {
					'max_length': '项目名不得超出200个字符长度',
				},
				'validators': [UniqueValidator(queryset=Projects.objects.all(), message='项目名已存在')]
			},
			# 'leader': {
			# 	'label': '项目负责人',
			# 	'help_text': '项目负责人',
			# 	'max_length': 50,
			# 	'error_messages': {
			# 		'max_length': '输入内容不得超出50个字符长度'
			# 	}
			# },
			'tester': {
				'label': '测试人员',
				'help_text': '测试人员',
				'max_length': 50,
				'error_messages': {
					'max_length': '输入内容不得超出50个字符长度'
				}
			},
			'programmer': {
				'label': '开发人员',
				'help_text': '开发人员',
				'max_length': 50,
				'error_messages': {
					'max_length': '输入内容不得超出50个字符长度'
				}
			},
			# 'publish_app': {
			# 	'label': '发布应用',
			# 	'help_text': '发布应用',
			# 	'max_length': 100,
			# 	'error_messages': {
			# 		'max_length': '输入内容不得超出100个字符长度'
			# 	}
			# },
			'desc': {
				'label': '简要描述',
				'help_text': '简要描述',
				'max_length': 200,
				'allow_blank': True,
				'error_messages': {
					'max_length': '输入内容不得超出200个字符长度'
				}
			},
			'create_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			}
		}

	def create(self, validate_data):
		# 在创建项目时，同时创建一个空的debugtalk.py文件
		project = super().create(validate_data)
		DebugTalks.objects.create(project=project)
		return project


# 获取项目下的接口
class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
	interfaces = InterfacesNamesModelSerializer(many=True, read_only=True)

	class Meta:
		model = Projects
		fields = ('interfaces', )


# 运行项目 获取环境变量
class ProjectsRunModelSerializer(serializers.ModelSerializer):
	env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID', write_only=True, validators=[validates.is_existed_env_id])

	class Meta:
		model = Projects
		fields = ('id', 'env_id')