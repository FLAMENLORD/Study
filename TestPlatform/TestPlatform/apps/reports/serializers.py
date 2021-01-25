from rest_framework import serializers

from utils import common
from .models import Reports


class ReportsModelSerializer(serializers.ModelSerializer):

	class Meta:
		model = Reports
		exclude = ('update_time',)

		extra_kwargs = {
			'create_time': {
				'format': common.datetime_fmt()
			},
			'html': {
				'write_only': True
			}
		}

