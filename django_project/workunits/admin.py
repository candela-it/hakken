from django.contrib import admin
from .models import (
    WorkUnit, Solution)


class WorkUnitAdmin(admin.ModelAdmin):
    pass

admin.site.register(WorkUnit, WorkUnitAdmin)


class SolutionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Solution, SolutionAdmin)
