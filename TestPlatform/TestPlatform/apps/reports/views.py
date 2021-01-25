import logging
import os
import json

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import action
from django.http.response import StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from django.conf import settings
from .models import Reports
from .serializers import ReportsModelSerializer
from .utils import get_file_content

logger = logging.getLogger('mytest')


class ReportsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericViewSet):
	queryset = Reports.objects.all()
	serializer_class = ReportsModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['create_time']

	def list(self, request, *args, **kwargs):
		response = super().list(self, request, *args, **kwargs)
		results = response.data['results']
		for i in results:
			i['result'] = 'Pass' if i['result'] else 'Faild'
		return response

	def retrieve(self, request, *args, **kwargs):
		response = super().retrieve(self, request, *args, **kwargs)
		response.data['summary'] = json.loads(response.data['summary'])
		return response

	@action(detail=True)
	def download(self, request, *args, **kwargs):
		# 获取Html源码
		instance = self.get_object()
		html = instance.html
		name = instance.name
		# 获取测试报告所属目录路径
		report_dir = settings.REPORT_DIR
		# 生成html文件，存放到reports目录下
		report_full_dir = os.path.join(report_dir, name) + '.html'
		if not os.path.exists(report_full_dir):
			with open(report_full_dir, 'w', encoding='utf-8') as file:
				file.write(html)

		response = StreamingHttpResponse(get_file_content(report_full_dir, 1024))
		html_file_name = escape_uri_path(name + '.html')
		# 添加响应头
		response['Content-Type'] = 'application/octet-stream'
		response['Content-Disposition'] = f"attachement; filename*='utf-8' {html_file_name}"

		return response

