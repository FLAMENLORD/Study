from rest_framework import serializers

from utils import common
from .models import Interfaces
from projects.models import Projects
from testcases.models import Testcases
from configures.models import Configures
from utils import validates


# 关联接口所属项目信息
class ProjectsInfoModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Projects
		fields = '__all__'


class InterfacesModelSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField()
	project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())

	class Meta:
		model = Interfaces
		exclude = ('update_time',)

		extra_kwargs = {
			'create_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			}
		}

	def create(self, validated_data):
		if 'project_id' in validated_data:
			project = validated_data.pop('project_id')
			validated_data['project'] = project
			return super().create(validated_data)

	def update(self, instance, validated_data):
		if 'project_id' in validated_data:
			project = validated_data.pop('project_id')
			validated_data['project'] = project
			return super().update(instance, validated_data)


# 根据接口ID映射所属项目
class ProjectByInterfaceIdModelSerializer(serializers.ModelSerializer):
	project = ProjectsInfoModelSerializer(read_only=True)

	class Meta:
		model = Interfaces
		fields = ('name', 'project')


# 关联接口下的用例信息
class TestcasesNamesModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Testcases
		fields = ('id', 'name')


class TestcasesByInterfaceIdModelSerializer(serializers.ModelSerializer):
	testcases = TestcasesNamesModelSerializer(many=True, read_only=True)

	class Meta:
		model = Interfaces
		fields = ('testcases', )


class ConfiguresNamesModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Configures
		fields = ('id', 'name')


class ConfiguresByInterfaceIdModelSerializer(serializers.ModelSerializer):
	configures = ConfiguresNamesModelSerializer(many=True, read_only=True)

	class Meta:
		model = Interfaces
		fields = ('configures', )


class InterfacesRunModelSerializer(serializers.ModelSerializer):
	env_id = serializers.IntegerField(label='环境变量ID', help_text='环境变量ID', write_only=True, validators=[validates.is_existed_env_id])

	class Meta:
		model = Interfaces
		fields = ('id', 'env_id')
