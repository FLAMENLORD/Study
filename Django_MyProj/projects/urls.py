from django.urls import path
from projects.views import index02_page, index03_page


urlpatterns = [
    path('index02/', index02_page),
    path('index03/', index03_page),
]