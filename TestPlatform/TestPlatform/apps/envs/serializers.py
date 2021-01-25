from rest_framework import serializers

from utils import common
from .models import Envs


class EnvsModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Envs
		exclude = ('update_time',)

		extra_kwargs = {
			'create_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			}
		}


class EnvsNamesModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = Envs
		fields = ('id', 'name')
