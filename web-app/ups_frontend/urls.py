from django.urls import path, include
from django.contrib import admin
from . import views
admin.autodiscover()
urlpatterns = [
    path('', views.login, name='login'),
    path('login/',views.login,name='login'),
    path('regist/',views.regist,name='regist'),
    path('authentication/',views.authentication, name = 'authentication'),
    path('user/',views.user,name='user'),
    path('addUser/',views.addUser,name='addUser'),
    path('logout/',views.logout,name='logout'),
    path('list/',views.list,name='list'),
    path('track/',views.track,name='track'),
    path('search/',views.search,name='search'),
    path('post/',views.post,name='post'),
    path('showitem/',views.showitem,name='showitem'),
    path('showhistory/',views.showhistory,name='showhistroy'),
    path('sendemail/',views.sendemail,name='sendemail'),
]
