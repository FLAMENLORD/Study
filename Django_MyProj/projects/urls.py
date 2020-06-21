from django.urls import path
# from projects.views import index02_page, index03_page, IndexPage
from projects import views


urlpatterns = [
    path('index02/', views.index02_page),
    path('index03/', views.index03_page),
    # 类视图定义路由
    # path函数的第二个参数为类视图名.as_view()
    # 可以使用<url类型转换器：路径参数名>
    # int、path、uuid、slug等
    # path('index04/<int:pk>/<username>/', views.IndexPage.as_view()),
    path('index04/', views.IndexPage.as_view()),
]