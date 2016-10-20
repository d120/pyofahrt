from django.contrib import admin
from .models import Ofahrt, Building, Location, Room

# Register your models here.

@admin.register(Ofahrt)
class OfahrtAdmin(admin.ModelAdmin):
    list_display = ["__str__", "begin_date", "end_date"]
    fieldsets = (
    ("Allgemeines", {
        "fields": ("begin_date", "end_date")
    }),
    ("Einstellungen", {
        "fields" : ("member_reg_open", "orga_reg_open", "workshop_reg_open", "max_members", "queue_tolerance" ,"self_participation")
    })
    )

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_filter = ('location',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_filter = ('building', 'usecase_sleep', 'usecase_workshop', 'usecase_meal', 'usecase_store', 'usecase_outside')
    list_display = ['__str__', 'capacity', 'usecase_sleep', 'usecase_workshop', 'usecase_meal', 'usecase_store', 'usecase_outside']
    save_as = True
    pass
