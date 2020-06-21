"""Django_MyProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# 导入视图函数
# from projects.views import index01_page, IndexPage
from projects import views

"""
urlpatterns为名称固定的列表，用于存放路由信息
列表中的元素个数就是路由条数
路由匹配规则：
    从上到下开始匹配
    一旦匹配成功，会自动调用path第二个参数所指定的视图函数
    一旦匹配成功，不会再往下匹配
    匹配不成功，则返回404
    路由信息，尽量使用/结尾
    可以在子应用中定义子路由，子应用名/urls.py来定义
    可以使用include来加载子路由，第一个参数为字符串（'子应用名.urls'）
    如果url第一部分匹配，则会将url剩下的部分拿到子路由中去匹配
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index01/', views.index01_page),
    path('index04/', views.IndexPage.as_view()),
    path('childproj/', include('projects.urls')),
]

