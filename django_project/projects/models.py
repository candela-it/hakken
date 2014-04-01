import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField


class Project(TimeStampedModel):
    """
    Hakken project base model
    """
    STATUS = Choices('deleted', 'archived', 'hidden', 'active')

    title = models.CharField(max_length=200, help_text='Title of the project')
    description = models.CharField(
        max_length=200, help_text='Short description of the project')
    creator = models.ForeignKey(
        'auth.User', help_text='Project was created by'
    )
    area_of_interest = models.MultiPolygonField(
        srid=4326, help_text='Geometry for the area of interest',
        blank=True, null=True
    )
    initial_zoom = models.IntegerField(
        help_text='Initial zoom level of a project'
    )
    status = StatusField()
    workflow = models.ForeignKey('projects.Workflow', blank=True, null=True)

    def __unicode__(self):
        return '{} - {}'.format(self.id, self.title)


class Workflow(models.Model):
    """
    Workflow defines how users progress through project
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    iteration = models.ManyToManyField(
        'projects.Iteration', through='IterationStep'
    )

    def __unicode__(self):
        return '{} - {}'.format(self.title, self.description)


class IterationStep(models.Model):
    """
    Each iteration in a workflow is defined by a position in the workflow
    """
    iteration_step = models.IntegerField(
        default=1, help_text='Priority of the iteration'
    )
    workflow = models.ForeignKey('projects.Workflow')
    iteration = models.ForeignKey('projects.Iteration')

    def __unicode__(self):
        return '{} - {} ({})'.format(
            self.workflow.id, self.iteration.id, self.iteration_step
        )


class Iteration(models.Model):
    """
    An iteration encapsulates a set of questions
    """
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField('projects.Answer', through='AnswerOrder')

    def __unicode__(self):
        return '{} - {}'.format(self.id, self.question)


class AnswerOrder(models.Model):
    """
    Answers can be ordered in a specific way
    """
    answer = models.ForeignKey('projects.Answer')
    iteration = models.ForeignKey('projects.Iteration')
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return '{} - {} ({})'.format(
            self.answer.id, self.iteration.id, self.rank
        )


class Answer(models.Model):
    """
    A possible answer
    """
    text = models.CharField(
        max_length=50, help_text='Actual answer, presented to the user'
    )
    value = models.IntegerField(
        default=0, help_text='Used to attach some value to the answer'
    )

    def __unicode__(self):
        return '{} - {}'.format(self.id, self.text)
