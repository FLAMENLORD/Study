from django.forms import model_to_dict
import datetime
from django.http import JsonResponse
from django.views import View
import json

from .models import Projects
from .serializers import ProjectModelSerializer


class ProjectsInfo(View):
    # 查询项目：id默认为空，id为空时，查询所有项目，否则查询指定项目详情
    def get(self, request, pk=None):
        qs = Projects.objects.all()
        serializer_obj = ProjectModelSerializer(instance=qs, many=True)
        return JsonResponse(serializer_obj.data, safe=False)

    # 创建项目：数据以json格式传入
    def post(self, request):
        res = {}
        try:
            serializer_obj = ProjectModelSerializer(request.data)
            if serializer_obj.is_valid():
                serializer_obj.save()
                res['msg'] = '接口信息创建成功'
            else:
                return JsonResponse(serializer_obj.errors, status=401, safe=False)
        except Exception as e:

            res['msg'] = f'接口信息创建失败：{e}'

        return JsonResponse(res)

    # 更新项目：传入需更新记录的id，修改数据以json形式传入
    def put(self, request, pk):
        update_data = json.loads(request.body)
        res = {}
        try:
            proj_obj = Projects.objects.get(id=pk)
            for key, value in update_data.items():
                print(key, value)

                proj_obj.key = value
            proj_obj.save()
            res['msg'] = '更新成功'
            res['code'] = 0
        except Exception as e:
            res['msg'] = '更新失败'
            res['code'] = 1
            print('项目创建失败：', e)
        return JsonResponse(res)

    # 删除项目：传入需删除记录的id
    def delete(self, requset, pk):
        res = {}
        try:
            proj_obj = Projects.objects.get(id=pk)
            proj_obj.delete()
            res['msg'] = '删除成功'
            res['code'] = 0
        except Exception as e:
            res['msg'] = '删除失败'
            res['code'] = 1
            print('项目删除失败：', e)
        return JsonResponse(res)
