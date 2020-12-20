# -*- coding: utf-8 -*-
# @Time    : 2020/12/20 下午5:04
# @Author  : zhongxin
# @Email   : 490336534@qq.com
# @File    : urls.py
from django.urls import path
from lists import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('new', views.new_list, name='new_list'),
    path('<int:list_id>/', views.view_list, name='view_list'),
    path('<int:list_id>/add_item', views.add_item, name='view_list')
]
