from django.contrib import admin

# Register.vue your models here.
from . import models

admin.site.register(models.User)
admin.site.register(models.Task)
admin.site.register(models.Project)
admin.site.register(models.Report)
admin.site.register(models.File)
