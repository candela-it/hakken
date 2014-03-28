import logging
logger = logging.getLogger(__name__)
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'adminhome.html'


class AddNew(TemplateView):
    template_name = 'admin_add.html'
