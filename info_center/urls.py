from django.conf.urls import patterns, url

import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^index$', views.index, name='index'),
    url(r'^fetion$', views.fetion, name='fetion'),
    url(r'^update/(?P<source>\w+)', views.update, ),
)
