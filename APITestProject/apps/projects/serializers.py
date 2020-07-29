from rest_framework import serializers
from .models import Projects
from interfaces.models import Interfaces


# 接口模型序列化器类
class InterfacesInfoModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Interfaces
		fields = '__all__'


class ProjectsModelSerializer(serializers.ModelSerializer):
	interfaces = InterfacesInfoModelSerializer(many=True, read_only=True)

	def validate_name(self, value):
		if 'test' in value:
			raise serializers.ValidationError("接口名称中不能包含'test'")
		return value

	class Meta:
		model = Projects
		fields = '__all__'
		read_only_fields = ('id', 'create_time', 'update_time')


# 根据项目ID映射接口信息
class InterfacesByProjectIdModelSerializer(serializers.ModelSerializer):
	interfaces = InterfacesInfoModelSerializer(many=True, read_only=True)

	class Meta:
		model = Projects
		fields = ('name', 'interfaces')