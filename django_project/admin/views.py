import logging
logger = logging.getLogger(__name__)
from django.views.generic.base import TemplateView
from django.views.generic import FormView, UpdateView, DetailView, ListView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from forms import ProjectFormStepOne, ProjectFormStepTwo, ProjectFormStepThree
from projects.models import Project


class AddNewStepOne(FormView):
    form_class = ProjectFormStepOne
    template_name = 'admin_add.html'

    def form_valid(self, form):
        self.project = form.save(commit=False)

        self.project.creator = self.request.user
        self.project.status = 'hidden'
        self.project.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, re-render the context data with the
        data-filled form and errors."""
        response = self.render_to_response(self.get_context_data(form=form))
        return response

    def get_success_url(self):
        return reverse('admin_add_two', kwargs={'pk': self.project.pk})


class AddNewStepTwo(UpdateView):
    form_class = ProjectFormStepTwo
    template_name = 'admin_add2.html'
    model = Project

    def form_valid(self, form):
        self.project = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_add_three', kwargs={'pk': self.project.pk})


class AddNewStepThree(UpdateView):
    form_class = ProjectFormStepThree
    template_name = 'admin_add3.html'
    model = Project

    def form_valid(self, form):
        self.project = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('admin_add_confirm', kwargs={'pk': self.project.pk})


class AddNewConfirm(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'admin_add_confirm.html'


class HomeView(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'adminhome.html'
