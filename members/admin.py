from django.contrib import admin
from .models import Member, FoodHandicaps
from . import admin_actions, admin_filters

# Register your models here.

admin.site.register(FoodHandicaps)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "email"]
    actions = [admin_actions.mail_export, admin_actions.move_to_queue, admin_actions.mark_participants_contributing_paid]
    list_display = ('first_name', 'last_name', 'gender', 'is_really_ersti', 'is_full_aged', 'queueinfo')
    list_filter = (admin_filters.MemberQueueFilter ,'gender', 'money_received', 'is_really_ersti', 'room')
    fieldsets = (
        ('Ofahrt', {
            'fields': ('base',)
        }),
        ('Formale Daten', {
            'fields': ('first_name', 'last_name', 'gender', 'birth_date', 'email'),
        }),
        ('Verpflegung', {
            'fields': ('food_preference', 'food_handicaps'),
        }),
        ('Status', {
            'fields': ('is_really_ersti', 'queue', 'queue_deadline', 'money_received'),
        }),
        ('Sonstiges', {
            'fields': ('room', 'free_text'),
        }),
    )

    def queueinfo(self, obj):
        if obj.money_received:
            return "festangemeldet"
        elif obj.queue:
            if obj.queue_deadline:
                time = obj.queue_deadline.strftime("%d.%m.%Y - %H:%M")
            else:
                time = "unbekannt"
            return "vorläufig (Geldeingang bis %s Uhr)" % time
        else:
            return "Warteschlange"
    queueinfo.short_description = "Liste"
