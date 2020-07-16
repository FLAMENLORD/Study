from django.http import JsonResponse,Http404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.views import Response
from rest_framework.views import status
from django.views import View
from django.forms import model_to_dict
from django_filters.rest_framework import DjangoFilterBackend

from .models import Interfaces
from .serializers import InterfaceModelSerializer
from projects.models import Projects


class InterfacesInfo(GenericAPIView):
	# 获取接口项目信息
	def get_project_info(self,proj_id):
		proj_obj=Projects.objects.get(id=proj_id)
		project_info=model_to_dict(proj_obj)
		return project_info

	# def get_object(self, pk):
	#     try:
	#         interfaces_obj = Interfaces.objects.get(id=pk)
	#     except Exception as e:
	#         res = {
	#             'msg': f'参数有误：{e}',
	#             'code': 0
	#         }
	#         raise Http404(res)
	#     return interfaces_obj

	# 查询接口信息：id默认为空
	# def get(self, request):
	#     res = {}
	#     qs = Interfaces.objects.all()
	#     name = request.query_params.get('name')
	#     if name:
	#         qs = qs.filter(name=name)
	#         InterfacesModelSerializer(instance=qs, many=True)
	#
	#     # Response第一个参数为，经过序列化后的数据（serializer_obj.data）
	#     # status指定响应状态码，默认为200
	#     return Response(res, status=status.HTTP_200_OK)

	# 指定queryset，当前接口中需要使用到的查询集
	queryset=Interfaces.objects.all()

	# 指定serializer_class，当前接口中需要使用到的序列化器类
	serializer_class=InterfacesModelSerializer

	# 指定使用的过滤引擎，如果多个过滤引擎，可以在列表中指定
	# 可以在全局settings.py配置文件中指定所有视图公用的过滤引擎，
	# 如果视图中未指定，则使用全局的过滤引擎，否则使用视图中指定的过滤引擎（即视图中的优先级更高）
	# 可在filter_backends指定排序功能
	filter_backends=[DjangoFilterBackend,OrderingFilter]

	# 指定需要进行过滤的字段，字段要与模型类中的字段名一致，精确匹配
	filter_fields=['name','leader','id']
	# 在ordering_fields指定排序字段的顺序
	# 前端在过滤时，需要使用ordering作为key，具体的排序字段作为value
	# 默认升序排序，降序排序在字段名前加 '-'
	ordering_fields=['name','id']

	def get(self,request):
		# 使用get_queryset()，获取查询集对象
		qs=self.get_queryset()

		# 调用filter_queryset()，需要传递一个查询集对象，返回一个查询集
		# qs = self.filter_queryset(qs)

		# 使用get_serializer()，调用序列化器类
		serializer_obj=self.get_serializer(isinstance=qs,many=True)
		return Response(serializer_obj.data,status=status.HTTP_200_OK)

	# 创建接口：数据以json格式传入
	def post(self,request):
		res={}
		try:
			serializer_obj=InterfacesModelSerializer(data=request.data)
			if serializer_obj.is_valid():
				serializer_obj.save()
				res['code']=0
				res['message']='接口信息创建成功'
				res['data']=serializer_obj.data
			else:
				res['message']=serializer_obj.errors
				return JsonResponse(res,status=401,safe=False)
		except Exception as e:
			res['code']=1
			res['message']=f'接口信息创建失败：{e}'
		return Response(res,status=status.HTTP_200_OK)

	# 更新接口信息：传入需更新记录的id，修改数据以json形式传入
	def put(self,request,pk):
		inter_obj=self.get_object(pk)
		res={}
		try:
			serializer_obj=InterfacesModelSerializer(instance=inter_obj,data=request.data,partial=True)
			if serializer_obj.is_valid():
				serializer_obj.save()
				res['code']=0
				res['message']='接口信息更新成功'
			else:
				res['message']=serializer_obj.errors
				return JsonResponse(res,status=401,safe=False)
		except Exception as e:
			res['code']=1
			res['message']=f'接口信息更新失败：{e}'
		return Response(res,status=status.HTTP_200_OK)

	# 删除接口：传入需删除记录的id
	def delete(self,requset,pk):
		res={}
		try:
			inter_obj=self.get_object(pk)
			inter_obj.delete()
			res['msg']='接口信息删除成功'
			res['code']=0
		except Exception as e:
			res['code']=1
			res['message']=f'接口信息删除失败：{e}'
		return Response(res,status=status.HTTP_200_OK)

