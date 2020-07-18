from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView, Response, status
from .models import Projects
from .serializers import ProjectModelSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# 导入自定义的分页引擎
from utils.pagination import MyPagination


class ProjectsInfo(GenericAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['name', 'tester', 'id']
    ordering_fields = ['name', 'id']

    def get(self, request, *args, **kwargs):
        # 传递查询集对象给filter_queryset()
        qs = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(qs)
        # # 判断是否指定分页引擎
        # if page is not None:
        #     # 调用序列化器，获取数据
        #     serializer_obj = self.get_serializer(instance=page, many=True)
        #
        #     # 将数据进行分页
        #     return self.get_paginated_response(serializer_obj.data)
        serializer_obj = self.get_serializer(instance=qs, many=True)
        return Response(serializer_obj.data, status=status.HTTP_200_OK)


    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)
    #
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
#
#
# # class ProjectsDetail(generics.RetrieveUpdateAPIView):
# #     queryset = Projects.objects.all()
# #     serializer_class = ProjectModelSerializer
#
#     # # 查询项目：id默认为空，id为空时，查询所有项目，否则查询指定项目详情
#     # def get(self, request, *args, **kwargs):
#     #     return self.retrieve(request, *args, **kwargs)
#     #
#     # # 创建项目：数据以json格式传入
#     # def post(self, request):
#     #     serializer_obj = self.get_serializer(data=request.data)
#     #     serializer_obj.is_valid(raise_exception=True)
#     #     serializer_obj.save()
#     #     return Response(serializer_obj.data, status=status.HTTP_200_OK)
#     #
#     # # 更新项目：传入需更新记录的id，修改数据以json形式传入
#     # def put(self, request, pk):
#     #     obj = self.get_object()
#     #     serializer_obj = self.get_serializer(instance=obj, data=request.data)
#     #     # 在视图中抛出的异常，DRF会自动处理，报错信息以json格式返回
#     #     serializer_obj.is_valid(raise_exception=True)
#     #     serializer_obj.save()
#     #     return Response(serializer_obj.data, status=status.HTTP_201_CREATED)
#     #
#     # # 删除项目：传入需删除记录的id
#     # def delete(self, requset, pk):
#     #     obj = self.get_object()
#     #     obj.delete()
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
#
