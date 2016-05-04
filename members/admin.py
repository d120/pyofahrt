from django.contrib import admin
from .models import Member, RoomAssignment, FoodHandicaps

# Register your models here.

admin.site.register(FoodHandicaps)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'money_received', 'is_really_ersti', 'is_full_aged')
    list_filter = ('gender', 'money_received', 'is_really_ersti')
    fieldsets = (
        ('Ofahrt', {
            'fields': ('base',)
        }),
        ('Formale Daten', {
            'fields': ('first_name', 'last_name', 'gender', 'birth_date'),
        }),
        ('Verpflegung', {
            'fields': ('food_preference', 'food_handicaps'),
        }),
        ('Status', {
            'fields': ('money_received', 'is_really_ersti'),
        }),
        ('Sonstiges', {
            'fields': ('free_text',),
        }),
    )


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):

    def get_members(self, obj):
        return ", ".join([str(t) for t in obj.members.all()])

    get_members.short_description = "Zugeteilte Personen"

    list_display = ['room', 'get_members']
    fieldsets = (
        ('Ofahrt', {
            'fields': ('base',)
        }),
        (None, {
            'fields': ('room', 'members'),
        }),
    )
    pass
