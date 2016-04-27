from django.contrib import admin
from workshops.models import Workshop

# Register your models here.

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    pass
