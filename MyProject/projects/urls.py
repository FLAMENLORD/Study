"""MyProject URL Configuration

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
from django.urls import path
from projects import views

# 继承ViewSet后，支持在路由表中指定请求方法与action的映射
# as_view接收一个字典，key为请求方法，value为请求动作
urlpatterns = [
	path('projects/', views.ProjectViewSet.as_view({
		'get': 'list', 'post': 'create'
	})),
	path('projects/<int:pk>', views.ProjectViewSet.as_view({
		'get': 'retrieve', 'put': 'update', 'delete': 'destory'
	})),
]
