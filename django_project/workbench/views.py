import logging
logger = logging.getLogger(__name__)
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (ListView, DetailView, RedirectView)
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from projects.models import Project
from workunits.models import WorkUnit, Solution


class SelectProject(ListView):
    context_object_name = 'projects'
    model = Project
    template_name = 'wb_select.html'
    queryset = Project.objects.all().filter(status='active')


class workProject(DetailView):
    context_object_name = 'project'
    model = Project
    template_name = 'wb_desk.html'

    def get_context_data(self, **kwargs):
        context = super(workProject, self).get_context_data(**kwargs)
        try:
            # if there is no speficifed WU
            # fetch first unlocked WU with highest zoom level
            if ('wu' in self.kwargs):
                wu = WorkUnit.objects.get(id=self.kwargs['wu'])
            else:
                wu = WorkUnit.objects.filter(
                    locked=False, project=self.object).order_by('-z')[:1].get()
            context['workunit'] = wu
            workunits = WorkUnit.objects.filter(
                project=self.object, locked=False)
            context['workunits'] = workunits
            # we need iteration that matches WU zoom
            # inital zoom -- 1st iteration
            # inital zoom + 1 -- 2nd iteration
            itnStep = wu.z - self.object.initial_zoom + 1
            itn = self.object.workflow.iterationstep_set.filter(
                iteration_step=itnStep).get().iteration
            context['iteration'] = itn
        except ObjectDoesNotExist:
            pass
        return context


class SubmitWorkunitSolution(RedirectView):
    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs.get('pk'))
        Solution.objects.create(
            workunit_id=request.POST['workunit'],
            answer_id=request.POST['answer'],
            user=request.user
        )

        return HttpResponseRedirect(
            reverse('wb_desk', kwargs={'pk': project.pk}))
