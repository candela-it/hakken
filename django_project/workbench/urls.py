from django.conf.urls import patterns, url
from .views import SelectProject


urlpatterns = patterns(
    '',
    # basic app views
    url(r'^workbench$', SelectProject.as_view(), name='wb_select'),
)
