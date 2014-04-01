from django.contrib import admin
from .models import (
    Project,
    Workflow,
    Iteration,
    IterationStep,
    Answer,
    AnswerOrder)

# class aModelAdmin(admin.ModelAdmin):
#    pass

# admin.site.register(aModel, aModelAdmin):
#    pass


class ProjectAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)


class WorkflowAdmin(admin.ModelAdmin):
    pass

admin.site.register(Workflow, WorkflowAdmin)


class IterationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Iteration, IterationAdmin)


class IterationStepAdmin(admin.ModelAdmin):
    pass

admin.site.register(IterationStep, IterationStepAdmin)


class AnswerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Answer, AnswerAdmin)


class AnswerOrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(AnswerOrder, AnswerOrderAdmin)
