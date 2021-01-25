import logging

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions

from .models import DebugTalks
from .serializers import DebugTalksModelSerializer

logger = logging.getLogger('mytest')


class DebugTalksViewSet(viewsets.ModelViewSet):
	queryset = DebugTalks.objects.all()
	serializer_class = DebugTalksModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['id', 'name', 'create_time']
