from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
from django.db.models import Q, Count,
import json
import string
import random

from .models import Projects
from interfaces.models import Interfaces


# 视图函数
# 第一个参数为HtpRequest对象或者HttpRequest子类的对象，无需手动传递，一般为request
# 一定要返回HttpResponse对象或者HttpResponse子类对象
def index01_page(request):
    return HttpResponse('<h2>Hello World，这是主路由</h2>')


def index02_page(request):
    return HttpResponse('<h2>测开4期，这是子路由1</h2>')


def index03_page(request):
    return HttpResponse('<h2>二鬼，这是子路由2</h2>')


class IndexPage(View):
    def get(self, request):
        qs = Projects.objects.filter(interfaces__name__regex='^[0-9]]')
        for item in qs:
            print(item.name)

        # qs = Projects.objects.filter(name__startswith='x').filter(programmer__contains='4')
        # qs = Projects.objects.filter(name__startswith='x', programmer__contains='4')

        qs = Projects.objects.filter(Q(leader__contains='1') | Q(programmer__contains='4'))
        qs = Projects.objects.annotate(Count('name'))
        # order_by排序，默认升序。使用 '-'，降序
        Projects.objects.all().order_by('-id', 'name')

        return HttpResponse('<h2>get请求</h2>')

    def put(self, request):
        # 方法一：
        proj_obj = Projects.objects.get(name='飞向月球计划')
        proj_obj.name = '驻扎广寒宫计划'
        proj_obj.save()

        # 方法二：
        Projects.objects.filter(name='Django学习计划').update(name='Django从入门到放弃')

        return HttpResponse('<h2>put请求</h2>')

    def post(self, request):
        # 定义一个包含所有大小写字母、数字的字符串
        one_str = string.ascii_letters + string.digits

        for i in range(20):
            one_list = [random.choice(one_str) for _ in range(5)]
            one_str_tmp = ' '.join(one_list)
            one_dict = {
                'name': one_str_tmp,
                'tester': f'xxx测试{i}',
                'desc': 'xxx描述',
                'projects_id': random.choice([1, 2, 3])
            }
            # **one_dict，拆成关键字参数
            one_obj = Interfaces.objects.create(**one_dict)

        return HttpResponse('<h2>post请求</h2>')

    def delete(self, request):
        proj_obj = Projects.objects.get(name='占领火星计划')
        proj_obj.delete()
        return HttpResponse('<h2>delete</h2>')
