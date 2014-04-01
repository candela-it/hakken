from django.conf.urls import patterns, url
from .views import (
    HomeView, AddNewStepOne, AddNewStepTwo, AddNewStepThree, AddNewConfirm)

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^project$', HomeView.as_view(), name='admin_home'),
    url(r'^project/add/$', AddNewStepOne.as_view(), name='admin_add'),
    url(r'^project/add/map/(?P<pk>\d+)/$', AddNewStepTwo.as_view(), name='admin_add_two'),
    url(r'^project/add/workflow/(?P<pk>\d+)/$', AddNewStepThree.as_view(), name='admin_add_three'),
    url(r'^project/add/confirm/(?P<pk>\d+)/$', AddNewConfirm.as_view(), name='admin_add_confirm'),
)
