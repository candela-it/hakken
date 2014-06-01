import logging
logger = logging.getLogger(__name__)

from django.db import models
from projects.utils import polyFromTile


class WorkUnit(models.Model):
    """
    WorkUnit model references a Project and basic information about grid
    """

    x = models.IntegerField(help_text='WorkUnit X coordinate on the grid')
    y = models.IntegerField(help_text='WorkUnit Y coordinate on the grid')
    z = models.IntegerField(help_text='WorkUnit Zoom level on the grid')
    project = models.ForeignKey('projects.Project')
    locked = models.BooleanField(help_text='Locked tile cannot be picked')

    def polygonWKT(self):
        return polyFromTile(self.x, self.y, self.z).wkt

    def __unicode__(self):
        return '{} ({}/{}/{})'.format(self.project, self.x, self.y, self.z)


class Solution(models.Model):
    """
    Answered question for the WorkUnit
    """
    workunit = models.ForeignKey('workunits.WorkUnit')
    answer = models.ForeignKey('projects.Answer')
    user = models.ForeignKey('auth.User')
