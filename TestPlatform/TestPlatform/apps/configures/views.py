import logging

from django.db.models import Count
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.views import Response
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Configures
from .serializers import ConfiguresModelSerializer

logger = logging.getLogger('mytest')


class ConfiguresViewSet(viewsets.ModelViewSet):
	queryset = Configures.objects.all()
	serializer_class = ConfiguresModelSerializer
	permission_classes = [permissions.IsAuthenticated]

	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['name', 'id']
	ordering_fields = ['id', 'name', 'create_time']