import logging
logger = logging.getLogger(__name__)
from django.views.generic import (ListView)
from projects.models import Project


# from .models import ...
class SelectProject(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'wb_select.html'
