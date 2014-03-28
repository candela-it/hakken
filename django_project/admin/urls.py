from django.conf.urls import patterns, url
from .views import HomeView, AddNew

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^admin$', HomeView.as_view(), name='admin_home'),
    url(r'^admin/add$', AddNew.as_view(), name='admin_add'),
)
