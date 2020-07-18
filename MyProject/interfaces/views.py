from django.http import JsonResponse, Http404
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView, Response, status
from django.views import View
from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend
from utils.pagination import MyPagination
from rest_framework import mixins
from .models import Interfaces
from .serializers import InterfacesModelSerializer
from rest_framework import generics


# 可以继承drf中的mixin拓展类
# 然后再继承GenericAPIView
# ListModelMixin -> list()，获取列表数据
# CreateModelMixin -> create()，创建数据
# RetrieveModelMixin -> retrieve()，获取详情数据
# UpdateModelMixin -> update()，更新数据
# DestoryModelMin -> destory()，删除数据
class InterfacesInfo(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    def get_object(self, pk):
        try:
            interfaces_obj = Interfaces.objects.get(id=pk)
        except Exception as e:
            res = {
                'msg': f'参数有误：{e}',
                'code': 0
            }
            raise Http404(res)
        return interfaces_obj

    # 将查询集提取到请求删除外部，提高性能，只需要查询一次即可完成多次操作
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['name', 'tester', 'id']
    ordering_fields = ['name', 'id']
    # 在视图中指定分页引擎类
    pagination_class = MyPagination

    # 查询接口
    def get(self, request, *args, **kwargs):
        # 传递查询集对象给filter_queryset()
        # qs = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(qs)
        # if page is not None:
        #     serializer_obj = self.get_serializer(instance=page, many=True)
        #     return self.get_paginated_response(serializer_obj.data)
        # serializer_obj = self.get_serializer(instance=qs, many=True)
        # return Response(serializer_obj.data, status=status.HTTP_200_OK)
        return self.get(request)

    # 创建接口
    def post(self, request, *args, **kwargs):
        # serializer_obj = self.get_serializer(data=request.data)
        # serializer_obj.is_valid(raise_exception=True)
        # serializer_obj.save()
        # return Response({'message': '新增成功'}, status=status.HTTP_200_OK)
        return self.create(request, *args, **kwargs)

    # 更新接口信息
    def put(self, request, pk):
        # inter_obj = self.get_object(pk)
        # serializer_obj = self.get_serializer(instance=inter_obj, data=request.data)
        # # 在视图中抛出的异常，DRF会自动处理，直接将报错信息以json形式返回
        # serializer_obj.is_valid(raise_exception=True)
        # serializer_obj.save()
        # return Response({'message': '更新成功'}, status=status.HTTP_200_OK)
        return self.update(request)

    # 删除接口：传入需删除记录的id
    def delete(self, requset, pk):
        # try:
        #     inter_obj = self.get_object(pk)
        #     inter_obj.delete()
        # except Exception as e:
        #     return Response({'errors': e}, status=status.HTTP_401_UNAUTHORIZED)
        # return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
        return self.delete(requset)


class InterfacesDetailView(generics.RetrieveUpdateAPIView):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer


from rest_framework import viewsets
# 只支持对get、post、put、delete、patch等请求方法
# 如果要支持action，需要继承ViewSet
# 当前ViewSet无法支持get_object()、filter_queryset()等
# GenericViewSet才支持分页、过滤、排序


# class InterfacesViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
#                         mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesModelSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ['name', 'tester', 'id']
    ordering_fields = ['name', 'id']
    # 请求方法与action一一映射
    # 这些方法称为action

    # def list(self, *args, **kwargs):
    #     pass

    # def retrieve(self, *args, **kwargs):
    #     pass

    # def create(self,*args,**kwargs):
    #     pass
    #
    # def update(self, *args, **kwargs):
    #     pass
    #
    # def destory(self, *args, **kwargs):
    #     pass