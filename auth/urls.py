from django.conf.urls import url

from auth import views

url_log_in = url(r'log-in/$', views.LogInView.as_view(), name='log_in')
url_log_out = url(r'log-out/$', views.log_out, name='log_out')
url_register = url(r'register/$', views.RegisterView.as_view(), name='register')
