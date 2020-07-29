from rest_framework import serializers
from .models import Interfaces
from projects.models import Projects


# 项目模型序列化器类
class ProjectsInfoModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Projects
		fields = '__all__'


class InterfacesModelSerializer(serializers.ModelSerializer):
	def validate_name(self, value):
		if 'test' in value:
			raise serializers.ValidationError('接口名称中不能包含"test"')
		return value

	class Meta:
		model = Interfaces
		fields = '__all__'


# 根据接口ID映射所属项目
class ProjectsByInterfaceIdModelSerializer(serializers.ModelSerializer):
	projects = ProjectsInfoModelSerializer(read_only=True)

	class Meta:
		model = Interfaces
		fields = ('name', 'projects')
