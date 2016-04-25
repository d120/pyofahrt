from django.contrib import admin
from .models import Ofahrt, Building, Location, Room, Setting

# Register your models here.

@admin.register(Ofahrt)
class OfahrtAdmin(admin.ModelAdmin):
    pass

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_filter = ('location',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_filter = ('building',)
    save_as = True
    pass

@admin.register(Setting)
class SettingsAdmin(admin.ModelAdmin):
    fields = ['readable', 'key', 'value']
    readonly_fields = ['key', 'readable']
    list_display = ['readable', 'value']
    pass

    def get_actions(self, request):
        actions = super(SettingsAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
