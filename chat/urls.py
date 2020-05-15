# chat/urls.py
from django.urls import path
from . import views
from django.conf.urls import url

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),


    #these two are alternative
    #path('<str:room_name>/', views.room, name='room'),
    url(r'(?P<room_name>\w+)/$', views.room, name='room'),
]
