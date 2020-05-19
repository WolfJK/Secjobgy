# coding: utf-8
# __author__: u"John"
from __future__ import unicode_literals, print_function
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name='login'),
    path('search', views.search, name='search'),
    path('new_emp', views.new_emp, name='new_emp'),
    path('new_emp_status', views.new_tmp_status, name="new_emp_status"),
    path('new_org', views.new_org, name='new_org'),
]
