from django.conf.urls import patterns, url
from iotshm_dashboard import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /iotshm_dashboard/5/
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # ex: /iotshm_dashboard/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /iotshm_dashboard/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)