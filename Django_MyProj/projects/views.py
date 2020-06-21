from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render
import json


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
    """
    类视图
    1. 一定要继承View的父类或者子类
    2. 可定义get、post、delete、put等方法，来实现GET、POST等请求
    3. 方法名固定切为小写
    4. 实例方法的第二个参数为HttpRequest对象
    """
    # def get(self, request, pk, username):
    #     """
    #     可使用url后面?的参数，称为query string查询字符串参数
    #     request.GET去获取参数字符串参数
    #     request.GET返回QueryDict对象，类似字典，支持字典中的所有操作
    #     request.GET[key]、request.GET.get(key)、request.GET.getlist()去获取参数值
    #     """
    #     return HttpResponse(f'<h2>get请求{username}</h2>')

    def get(self, request):
        data = [
            {
                'project_name': '王者项目',
                'leader': 'ergui',
                'app_name': '王者农药'
            },
            {
                'project_name': '活到最后项目',
                'leader': 'star',
                'app_name': '吃鸡'
            }
        ]
        # 前后端不分离
        # render()主要用于渲染模板，生成一个html页面，第一个参数为request，第二个参数为在templates目录下的模板名，第三个参数为context，只能传字典
        # return render(request, 'demo.html')
        # locals()，获取当前命名空间中的所有变量值，存放在一个字典中
        # return render(request, 'demo.html', locals())

        # 前后端分离
        # JsonResponse是HttpResponse的子类，第一个参数为字典或者嵌套字典的列表，如果使用非字典格式，需设置safe为False
        return JsonResponse(data, safe=False)

    def put(self, request):
        """
        HttpResponse对象，第一个参数为字符串类型或字节型参数，会将字符串内容返回到前端
        可以使用content_type来传递内容类型
        可以使用status参数来指定响应状态码
        """
        data = "{'name': 'ergui', 'age': 18}"
        return HttpResponse(data, content_type='application/json', status=200)

    def post(self, request, pk, username):
        """
        可以使用request.POST方法，获取application/x-www-form-urlencoded类型的参数
        可以使用request.body方法，获取application/json类型的参数
        可以使用request.META方法，获取请求头参数，key为HTTP_请求头key的大写
        """
        data_dict = json.loads(request.body, encoding='utf-8')
        return HttpResponse(f'<h2>post请求{data_dict["name"]}</h2>')

    def delete(self, request, pk, username):
        return HttpResponse('<h2>delete</h2>')


# class IndexPage(View):
#     def get(self, request):
#         data = [
#             {
#                 'project_name': '王者项目',
#                 'leader': 'ergui',
#                 'app_name': '王者农药'
#             },
#             {
#                 'project_name': '活到最后项目',
#                 'leader': 'star',
#                 'app_name': '吃鸡'
#             }
#         ]
#         # JsonResponse是HttpResponse的子类，第一个参数为字典或者嵌套字典的列表，如果使用非字典格式，需设置safe为False
#         return JsonResponse(data, safe=False)


# industry_list = [
# {
# "parent_ind" : "女装",
# "name" : "连衣裙"
# },
# {
# "name": "女装"
# },
# {
# "parent_ind" : "女装",
# "name" : "半身裙"
# },
# {
# "parent_ind" : "女装",
# "name" : "A字裙"
# },
# {
# "name": "数码"
# },
# {
# "parent_ind" : "数码",
# "name": "电脑配件"
# },
# {
# "parent_ind" : "电脑配件",
# "name": "内存"
# },
# ]
#
# key = []
# data_a = {}
# data_b = {}
# for i in industry_list:
#     if len(i) == 1:
#         key.append(i['name'])
#     elif i['parent_ind'] == "女装":
#          data_a.update({i['name']: {}})
#     elif i['parent_ind'] == "数码":
#         data_b.update({i['name']: {}})
#     elif i['parent_ind'] in data_b.keys():
#         data_b[i['parent_ind']].update({i['name']: {}})
# res = {
#     key[0]: data_a,
#     key[1]: data_b
# }
# print(res)


# input_str = 'ac'
# sum_time = 0
#
# for i in range(len(input_str)+1):
#     wait_time = (i-1)*2
#     click_time = i
#     sum_time += click_time + wait_time
# print(sum_time)
