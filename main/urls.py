from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='home'),
    path('index', views.index, name='home'),
    path('directory', views.directory, name='directory')
]