from django.conf.urls import patterns, url
from .views import (
    SelectProject, workProject, SubmitWorkunitSolution)


urlpatterns = patterns(
    '',
    # basic app views
    url(r'^workbench$', SelectProject.as_view(), name='wb_select'),
    url(r'^workbench/(?P<pk>\d+)/$', workProject.as_view(), name='wb_desk'),
    url(
        r'^workbench/submit/(?P<pk>\d+)/$',
        SubmitWorkunitSolution.as_view(), name='wb_submit'),
)
