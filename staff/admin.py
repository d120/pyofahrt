from django.contrib import admin
from .models import WorkshopCandidate, OrgaCandidate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType




# Register your models here.
admin.site.register(WorkshopCandidate)

class OrgaCandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'get_orga_jobs']

    def get_orga_jobs(self, obj):
        return ", ".join([str(t) for t in obj.orga_for.all()])
    get_orga_jobs.short_description = "Gewünschte Orgajobs"
admin.site.register(OrgaCandidate, OrgaCandidateAdmin)


class GroupAdmin(admin.ModelAdmin):
    actions = ['enable_reg', 'disable_reg']
    list_display = ['name', 'reg_enabled']

    def reg_enabled(self, obj):
        return Permission.objects.get(codename="group_full") not in obj.permissions.all()

    reg_enabled.short_description = "Registrierung möglich?"
    reg_enabled.boolean = True


    def enable_reg(self, request, queryset):
        for x in queryset.all():
            x.permissions = x.permissions.all().exclude(codename="group_full")


    def disable_reg(self, request, queryset):
        for x in queryset.all():
            x.permissions.add(Permission.objects.get(codename="group_full"))

    enable_reg.short_description = "Registrierung ermöglichen"
    disable_reg.short_description = "Registrierung verbieten"

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
