from rest_framework import serializers

from projects.models import Projects
from interfaces.models import Interfaces
from envs.models import Envs

def is_existed_project_id(value):
	"""
	校验项目id是否存在
	:param value:
	:return:
	"""

	if not Projects.objects.filter(id=value).exists():
		raise serializers.ValidationError('项目ID不存在')


def is_existed_interface_id(value):
	"""
	校验项目id是否存在
	:param value:
	:return:
	"""

	if not Interfaces.objects.filter(id=value).exists():
		raise serializers.ValidationError('接口ID不存在')


def is_existed_env_id(value):
	"""
	校验环境变量id是否存在
	:param value:
	:return:
	"""

	if not Envs.objects.filter(id=value).exists():
		raise serializers.ValidationError('环境变量ID不存在')