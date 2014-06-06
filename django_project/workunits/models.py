import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.utils import polyFromTile, deg2num


class WorkUnit(models.Model):
    """
    WorkUnit model references a Project and basic information about grid
    """

    x = models.IntegerField(help_text='WorkUnit X coordinate on the grid')
    y = models.IntegerField(help_text='WorkUnit Y coordinate on the grid')
    z = models.IntegerField(help_text='WorkUnit Zoom level on the grid')
    polygon = models.PolygonField(
        srid=4326, help_text='Geometry for the workunit',
        blank=True, null=True
    )
    project = models.ForeignKey('projects.Project')
    locked = models.BooleanField(help_text='Locked tile cannot be picked')

    objects = models.GeoManager()

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


@receiver(post_save, sender=Solution)
def checkToLockTile(sender, instance, **kwargs):
    deltaZoom = instance.workunit.z - instance.workunit.project.initial_zoom
    solutionCount = Solution.objects.filter(workunit=instance.workunit).count()
    # if delta is 0, we are on first iteration
    if deltaZoom == 0:
        # if there are 3 solutions, lock tile as we consider it solved
        if solutionCount == 3:
            WorkUnit.objects.filter(
                pk=instance.workunit.id).update(locked=True)
            positiveCount = Solution.objects.filter(
                workunit=instance.workunit, answer__value=1).count()
            # if there are more than 1(50%) positive answers, create tiles
            # for next zoom level and iteration
            if positiveCount > 1:
                zoom = instance.workunit.z + 1
                poly = polyFromTile(
                    instance.workunit.x,
                    instance.workunit.y,
                    instance.workunit.z
                )
                bbox = poly.extent
                bottomleft = deg2num(bbox[1], bbox[0], zoom)
                topright = deg2num(bbox[3], bbox[2], zoom)
                for x in range(bottomleft[0], topright[0]):
                    for y in range(topright[1], bottomleft[1]):
                        WorkUnit.objects.create(
                            x=x,
                            y=y,
                            z=zoom,
                            project=instance.workunit.project,
                            locked=False
                        )
    else:
        if solutionCount == 5:
            WorkUnit.objects.filter(
                pk=instance.workunit.id).update(locked=True)
