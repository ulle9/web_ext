from django.contrib import admin
from .models import Exteors
# Articles

class Exteors_ext(admin.ModelAdmin):
    readonly_fields = ('date_create', 'date_update')

admin.site.register(Exteors, Exteors_ext)
# admin.site.register(Articles)
# admin.site.register(Exteors)
