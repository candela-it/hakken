from django.conf.urls import patterns, url
from .views import HomeView

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^admin$', HomeView.as_view(), name='admin_home'),
)
