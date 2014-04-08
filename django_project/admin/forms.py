import logging
logger = logging.getLogger(__name__)

import django.forms as forms
import django.contrib.gis as gisforms
from projects.models import Project


class CustomOLWidget(gisforms.forms.OpenLayersWidget):
    template_name = 'OLWidget.html'


class ProjectFormStepOne(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'initial_zoom']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter project title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter project description'}),
            'initial_zoom': forms.TextInput(
                attrs={'placeholder': 'Enter default zoom level'}),
        }


class ProjectFormStepTwo(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['area_of_interest']
        widgets = {
            'area_of_interest': CustomOLWidget()
        }


class ProjectFormStepThree(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['workflow']
        widgets = {
            'workflow': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ProjectFormStepThree, self).__init__(*args, **kwargs)
        self.fields['workflow'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['workflow'].widget.choices = self.fields['workflow'].choices
