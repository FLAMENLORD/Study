import logging
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import Response

from .models import Envs
from .serializers import EnvsModelSerializer, EnvsNamesModelSerializer

logger = logging.getLogger('mytest')


class EnvsViewSet(viewsets.ModelViewSet):
	queryset = Envs.objects.all()
	serializer_class = EnvsModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['id', 'name', 'create_time']

	# 查询环境配置名称列表
	@action(methods=['get'], detail=False)
	def names(self, request, *args, **kwargs):
		qs = self.get_queryset()
		return Response(self.get_serializer(qs, many=True).data)

	def get_serializer_class(self):
		return EnvsNamesModelSerializer if self.action == 'names' else self.serializer_class
