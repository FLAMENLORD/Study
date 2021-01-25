from rest_framework import serializers

from .models import Testcases
from interfaces.models import Interfaces
from projects.models import Projects
from configures.models import Configures
from utils import validates


class InterfaceInfoModelSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
	project_id = serializers.PrimaryKeyRelatedField(label='所属项目ID', help_text='所属项目ID', read_only=True)
	pid = serializers.IntegerField(label='所属项目ID', help_text='所属项目ID', write_only=True, validators=[validates.is_existed_project_id])
	iid = serializers.IntegerField(label='所属接口ID', help_text='所属接口ID', write_only=True, validators=[validates.is_existed_interface_id])

	class Meta:
		model = Interfaces
		fields = ('pid', 'project', 'iid', 'name', 'project_id', 'id')

		extra_kwargs = {
			'name': {
				'read_only': True
			}
		}

	def validate(self, attrs):
		pid = attrs.get('pid')
		iid = attrs.get('iid')
		if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
			raise serializers.ValidationError('所属项目ID与接口ID不匹配')
		return attrs


class TestcasesModelSerializer(serializers.ModelSerializer):
	interface = InterfaceInfoModelSerializer()

	class Meta:
		model = Testcases
		exclude = ('update_time', 'create_time')

	def create(self, validated_data):
		validated_data['interface_id'] = validated_data.pop('interface').get('iid')
		return super().create(validated_data)

	def update(self, instance, validated_data):
		validated_data['interface_id'] = validated_data.pop('interface').get('iid')
		return super().update(instance, validated_data)


class TestcasesRunModelSerializer(serializers.ModelSerializer):
	env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID', write_only=True, validators=[validates.is_existed_env_id])

	class Meta:
		model = Testcases
		fields = ('id', 'env_id')
