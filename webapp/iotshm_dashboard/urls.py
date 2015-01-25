from django.conf.urls import patterns, url
from iotshm_dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^aboutiotshm/$', views.about, name='about'),
    url(r'^contactus/$', views.contact, name='contactus'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
)