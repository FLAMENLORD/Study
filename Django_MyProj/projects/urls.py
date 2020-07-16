from django.urls import path
# from projects.views import index02_page, index03_page, IndexPage
from projects import views


urlpatterns = [
    path('projectsDetail/', views.Projects.as_view()),
    path('projectsDetail/<int:pk>', views.Projects.as_view()),
]