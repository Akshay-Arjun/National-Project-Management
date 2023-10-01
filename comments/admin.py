from django.contrib import admin
from . import models

admin.site.register(models.TaskComment)
admin.site.register(models.ProjectComment)
