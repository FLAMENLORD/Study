from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
from django.db import connection
import json

from .models import Projects


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
        Projects.objects.filter(name='占领火星计划')

        # 方法一：
        Projects.objects.get(project_id=17)

        # 方法二：
        Projects.objects.filter(name='占领火星计划')

        # 方法三：
        Projects.objects.exclude(name='Django学习计划')

        # 方法四：
        res = Projects.objects.all()

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
        # 方法一：
        proj_obj = Projects(name='飞向月球计划', leader='ergui', tester='测试1', programmer='研发1')
        proj_obj.save()

        # 方法二：
        Projects.objects.create(name='占领火星计划', leader='ergui', tester='测试2', programmer='研发2')
        Projects.objects.create(name='Django学习计划', leader='ergui', tester='测试2', programmer='研发2')

        return HttpResponse('<h2>post请求</h2>')

    def delete(self, request):
        proj_obj = Projects.objects.get(name='占领火星计划')
        proj_obj.delete()
        return HttpResponse('<h2>delete</h2>')
