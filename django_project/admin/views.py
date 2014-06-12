import logging
logger = logging.getLogger(__name__)
from django.views.generic import (
    FormView, UpdateView, DetailView, ListView, RedirectView)
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Count, Max

from djgeojson.serializers import Serializer as GeoJSONSerializer

from .forms import ProjectFormStepOne, ProjectFormStepTwo, ProjectFormStepThree
from projects.models import Project
from workunits.models import WorkUnit
from projects.utils import deg2num, polyFromTile


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

    def get_context_data(self, **kwargs):
        context = super(AddNewConfirm, self).get_context_data(**kwargs)
        workunits = WorkUnit.objects.filter(project=self.object)
        context['workunits'] = workunits
        return context


class HomeView(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'adminhome.html'


class PublishProject(RedirectView):

    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs.get('pk'))
        if project.canBePublished:
            project.status = 'active'
            zoom = project.initial_zoom
            bbox = project.area_of_interest.envelope.extent
            bottomleft = deg2num(bbox[1], bbox[0], zoom)
            topright = deg2num(bbox[3], bbox[2], zoom)
            for x in range(bottomleft[0], topright[0] + 1):
                for y in range(topright[1], bottomleft[1] + 1):
                    poly = polyFromTile(x, y, zoom)
                    if (poly.within(project.area_of_interest) or
                            poly.intersects(project.area_of_interest)):
                        WorkUnit.objects.create(
                            x=x,
                            y=y,
                            z=zoom,
                            project=project,
                            locked=False,
                            polygon=poly
                        )
            project.save()

        return HttpResponseRedirect(
            reverse('admin_add_confirm', kwargs={'pk': project.pk}))


class DownloadRequest(BaseDetailView):
    model = Project

    def render_to_response(self, context):
        project = context['object']
        #no questions asked!
        workunits = (
            project.workunit_set
            .values('solution__answer__value', 'x', 'y', 'z', 'polygon')
            .annotate(
                answ=Count('solution__answer__value'),
                anws_val=Max('solution__answer__value')
            ).filter(anws_val__isnull=False)
        )
        area = GeoJSONSerializer().serialize(
            workunits,
            use_natural_keys=True, geometry_field='polygon',
            properties=['x', 'y', 'z', 'answ', 'anws_val'])

        return self.json_response(
            content=area,
            filename=project.title
        )

    def json_response(self, content, filename, **httpresponse_kwargs):
        response = HttpResponse(
            content, content_type='application/json', **httpresponse_kwargs
        )

        response['Content-Disposition'] = '{}; filename="{}.geojson"'.format(
            'attachment', filename)

        return response
