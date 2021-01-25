from rest_framework import serializers

from utils import common
from .models import DebugTalks


class DebugTalksModelSerializer(serializers.ModelSerializer):
	project = serializers.StringRelatedField()

	class Meta:
		model = DebugTalks
		exclude = ('update_time',)

		extra_kwargs = {
			'create_time': {
				'read_only': True,
				'format': common.datetime_fmt()
			}
		}
