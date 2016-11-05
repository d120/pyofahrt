from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "access_for_list", "responsible_for_list"]
    list_filter = ["access_for", "responsible_for"]


    def access_for_list(self, obj):
        return ", ".join([str(t) for t in obj.access_for.all()])
    access_for_list.short_description = "Zugangsberechtigt"

    def responsible_for_list(self, obj):
        return ", ".join([str(t) for t in obj.responsible_for.all()])
    responsible_for_list.short_description = "Hauptzuständig"