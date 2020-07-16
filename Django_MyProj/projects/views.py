from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView, Response, status
from rest_framework.generics import GenericAPIView

from django.views import View
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Count
import json
import string
import random

from .models import Projects
from interfaces.models import Interfaces
from .serializers import ProjectModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class Projects(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer
    # 指定过滤引擎
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'tester', 'leader', 'programmer']
    ordering_fields = ['name', 'create_time', 'id']

    def get(self, request):
        qs = self.filter_queryset(self.get_queryset())
        serializer_obj = self.get_serializer(instance=qs, many=True)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer_obj = ProjectModelSerializer(data=request.data)
        if serializer_obj.is_valid():
            serializer_obj.save()
        else:
            return Response(serializer_obj.errors, status=status.HTTP_200_OK)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     proj_obj = Projects.objects.get(id=pk)
    #     serializer_obj = ProjectModelSerializer(instance=proj_obj, data=request.data, partial=True)
    #     if serializer_obj.is_valid():
    #         serializer_obj.save()
    #     else:
    #         return Response(serializer_obj.errors, status=status.HTTP_200_OK)
    #     return Response(serializer_obj.data, status=status.HTTP_200_OK)