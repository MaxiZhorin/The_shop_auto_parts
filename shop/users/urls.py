"""market URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^login_basket/$', views.LoginFormViewBasket.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^register/$', views.register, name='register'),
    url(r'^lk/$', views.lk, name='lk'),
    url(r'^reset/$', views.reset_password, name='reset'),
    url(r'^reset_done/$', views.reset_password_done, name='reset'),
    # url('^', include('django.contrib.auth.urls')),
    url(r'^order/(?P<order_id>\w+)/$', views.lk_order, name='lk_order'),
    url(r'^password_change/$', views.password_change, name='password change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),






]
