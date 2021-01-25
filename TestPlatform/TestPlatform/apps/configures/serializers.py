from rest_framework import serializers

from utils import common
from .models import Configures
from projects.models import Projects
from interfaces.models import Interfaces


class InterfaceInfoModelSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')

	class Meta:
		model = Interfaces
		fields = ('name', 'project')


class ConfiguresModelSerializer(serializers.ModelSerializer):
	interface = InterfaceInfoModelSerializer(read_only=True)

	class Meta:
		model = Configures
		fields = ('id', 'name', 'author', 'interface', )

	# 	extra_kwargs = {
	# 		'create_time': {
	# 			'read_only': True,
	# 			'format': common.datetime_fmt()
	# 		},
	# 		'update_time': {
	# 			'read_only': True,
	# 			'format': common.datetime_fmt()
	# 		},
	# 		# 'include': {
	# 		# 	# 'write_only': True
	# 		# }
	# 	}
	#
	# def create(self, validated_data):
	# 	if 'project_id' in validated_data:
	# 		project = validated_data.pop('project_id')
	# 		validated_data['project'] = project
	# 		return super().create(validated_data)
	#
	# def update(self, instance, validated_data):
	# 	if 'project_id' in validated_data:
	# 		project = validated_data.pop('project_id')
	# 		validated_data['project'] = project
	# 		return super().update(instance, validated_data)
	#
