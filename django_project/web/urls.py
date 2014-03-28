from django.conf.urls import patterns, url
from .views import HomeView, LogoutUser


urlpatterns = patterns(
    '',
    # basic app views
    url(r'^$', HomeView.as_view(), name='homeview'),
    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
