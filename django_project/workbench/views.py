import logging
logger = logging.getLogger(__name__)
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import (ListView, DetailView, RedirectView)
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from projects.models import Project, Answer
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
            wu = WorkUnit.objects.filter(
                locked=False, project=self.object)[:1].get()
            context['workunit'] = wu
            itn = self.object.workflow.iteration.exclude(
                id__in=Solution.objects.filter(workunit=wu).values_list(
                    'answer__iteration__id', flat=True))[:1].get()
            context['iteration'] = itn
        except ObjectDoesNotExist:
            pass
        return context


class SubmitWorkunitSolution(RedirectView):
    def get(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs.get('pk'))
        wu = WorkUnit.objects.get(pk=request.POST['workunit'])
        anw = Answer.objects.get(pk=request.POST['answer'])
        solution = Solution(workunit=wu, answer=anw, user=request.user)
        solution.save()
        try:
            project.workflow.iteration.exclude(
                id__in=Solution.objects.filter(workunit=wu).values_list(
                    'answer__iteration__id', flat=True)).get()
        except ObjectDoesNotExist:
            wu.locked = True
            wu.save()
            try:
                WorkUnit.objects.filter(
                    locked=False, project=project)[:1].get()
            except ObjectDoesNotExist:
                project.status = 'finished'
                project.save()
                return HttpResponseRedirect(
                    reverse('wb_select'))

        return HttpResponseRedirect(
            reverse('wb_desk', kwargs={'pk': project.pk}))
