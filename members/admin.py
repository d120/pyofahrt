from django.contrib import admin
from .models import Member, FoodHandicaps

# Register your models here.

admin.site.register(FoodHandicaps)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'money_received', 'is_really_ersti', 'is_full_aged')
    list_filter = ('gender', 'money_received', 'is_really_ersti', 'room')
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
            'fields': ('room', 'free_text'),
        }),
    )
