from django.contrib import admin
from .models import WorkshopCandidate, OrgaCandidate
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import constants as messages
from django.core.mail import EmailMessage
from random import choice
from string import ascii_uppercase
from pyofahrt import settings

def randomword(length):
    return ''.join(choice(ascii_uppercase) for i in range(length))


# Register your models here.
class WorkshopCandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    actions = ['convert_to_account']

    def convert_to_account(self, request, queryset):
        errors = []
        success = []
        for user in queryset:
            accounts_found = User.objects.filter(email = user.email).count() + User.objects.filter(first_name = user.first_name, last_name = user.last_name).count()
            if accounts_found > 0:
                errors.append(user.__str__())
            else:
                username = user.first_name[0] + user.last_name
                username = username.lower()
                success.append(user.__str__())
                password = randomword(15)
                u = User.objects.create_user(username, user.email, None)
                u.first_name = user.first_name
                u.last_name = user.last_name
                u.is_staff = False
                u.is_active = True
                password = User.objects.make_random_password()
                u.set_password(password)

                workshopgroup = Group.objects.all().get(name="Workshop-Anbieter")
                u.groups.add(workshopgroup)

                u.save()
                user.delete()

                mail = EmailMessage()
                mail.subject = settings.MAIL_WORKSHOPSIGNUP_SUBJECT
                mail.body = settings.MAIL_WORKSHOPSIGNUP_TEXT % {'name' : user.first_name, 'username' : username, 'password' : password}
                mail.to = [u.email]
                mail.send()

        if len(errors) == 0:
            self.message_user(request, "Alle ausgewählten Bewerber wurden erfolgreich in pyofahrt-Accounts konvertiert.")
        else:
            if len(success) > 0 :
                self.message_user(request, "Die folgenden Bewerber wurden erfolgreich in einen pyofahrt-Account konvertiert: " + ", ".join(success))
            self.message_user(request, "Die folgenden Bewerber konnten nicht in einen pyofahrt-Account konvertiert werden, da sie Duplikaten entsprechen würden: " + ", ".join(errors), messages.ERROR)
        if len(success) > 0:
            self.message_user(request, "Vergiss nicht, die neuen Workshopanbieter in die Mailingliste ofahrt-workshops@d120.de aufzunehmen!", messages.WARNING)
    convert_to_account.short_description = "Bewerbung zu pyofahrt-Account konvertieren"


admin.site.register(WorkshopCandidate, WorkshopCandidateAdmin)

class OrgaCandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'get_orga_jobs']
    actions = ['convert_to_account']

    def get_orga_jobs(self, obj):
        return ", ".join([str(t) for t in obj.orga_for.all()])
    get_orga_jobs.short_description = "Gewünschte Orgajobs"

    def convert_to_account(self, request, queryset):
        errors = []
        success = []
        for user in queryset:
            accounts_found = User.objects.filter(email = user.email).count() + User.objects.filter(first_name = user.first_name, last_name = user.last_name).count()
            if accounts_found > 0:
                errors.append(user.__str__())
            else:
                username = user.first_name[0] + user.last_name
                username = username.lower()
                success.append(user.__str__())
                u = User.objects.create_user(username, user.email, None)
                u.first_name = user.first_name
                u.last_name = user.last_name
                u.is_staff = True
                u.is_active = True
                password = User.objects.make_random_password()
                u.set_password(password)
                u.save()
                for group in user.orga_for.all():
                    u.groups.add(group)
                user.delete()


                mail = EmailMessage()
                mail.subject = settings.MAIL_ORGASIGNUP_SUBJECT
                mail.body = settings.MAIL_ORGASIGNUP_TEXT % {'name' : user.first_name, 'username' : username, 'password' : password}
                mail.to = [u.email]
                mail.send()


        if len(errors) == 0:
            self.message_user(request, "Alle ausgewählten Bewerber wurden erfolgreich in pyofahrt-Accounts konvertiert.")
        else:
            if len(success) > 0 :
                self.message_user(request, "Die folgenden Bewerber wurden erfolgreich in einen pyofahrt-Account konvertiert: " + ", ".join(success))
            self.message_user(request, "Die folgenden Bewerber konnten nicht in einen pyofahrt-Account konvertiert werden, da sie Duplikaten entsprechen würden: " + ", ".join(errors), messages.ERROR)
        if len(success) > 0:
            self.message_user(request, "Vergiss nicht, die neuen Orgas in die Mailingliste ofahrt@d120.de aufzunehmen!", messages.WARNING)
    convert_to_account.short_description = "Bewerbung zu pyofahrt-Account konvertieren"


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
