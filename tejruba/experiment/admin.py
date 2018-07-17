from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Experiment)
admin.site.register(models.Useful)
admin.site.register(models.NotUseful)