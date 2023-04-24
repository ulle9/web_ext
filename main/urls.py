from django.urls import path
from . import views
urlpatterns = [
    path('index', views.index, name='home'),
    path('about', views.about, name='about')
]