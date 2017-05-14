"""sender_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from send_core import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^get/functions/$', views.get_functions),
    url(r'^user/whoami/$', views.whoami),
    url(r'^user/login/$', views.login),
    url(r'^user/logout/$', views.logout),
    url(r'^user/register/$', views.register),
    url(r'^get/status/(?P<target>\w+)/$', views.status),
    url(r'^get/function/form/(?P<target>\d+)/$', views.get_function_form),
    url(r'^user/username/valid/$', views.username_valid),
    url(r'^user/email/valid/$', views.email_valid),
    url(r'^user/code/valid/$', views.code_valid),
    url(r'^user/task/$', views.task),
    url(r'^task/create/$', views.task_create),
    url(r'^task/detail/(?P<target>\d+)/$', views.task_detail),
    url(r'^task/change/$', views.task_change),
    url(r'^task/delete/(?P<target>\d+)/$', views.task_delete),
    url(r'^task/log/(?P<target>\d+)/$', views.task_log),
]
