from django.http import HttpResponse


def index01_page(request):
    return HttpResponse('<h2>Hello World，这是主路由</h2>')


def index02_page(request):
    return HttpResponse('<h2>测开4期，这是子路由1</h2>')


def index03_page(request):
    return HttpResponse('<h2>二鬼，这是子路由2</h2>')
#
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
