from django.contrib import admin
from .models import WorkshopCandidate, OrgaCandidate
from django.contrib.auth.models import Group, Permission, User
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages import constants as messages
from django.core.mail import send_mail

from random import choice
from string import ascii_uppercase

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
                u = User.objects.create_user(username, user.email, password)
                u.first_name = user.first_name
                u.last_name = user.last_name
                u.is_staff = False
                u.is_active = True
                u.save()
                user.delete()
                send_mail("Willkommen als Workshopanbieter bei der Ofahrt!", "Hallo " + user.first_name +",\n\nwillkommen als Workshopanbieter der Ofahrt! Mit dem Erhalt dieser Email wurde den Account in pyofahrt, unserem Verwaltungstool zur Planung uns Strukturierung der OFahrt, freigeschaltet. Im folgenden findest du deine Logindaten.\n\npyofahrt: http://d120.de/ofahrt\nName: " + username + "\nPasswort: " + password + "\n\nIm Adminmenü kannst du dein Passwort jederzeit ändern. Du solltest desweiteren zeitnah auf unsere Mailingliste ofahrt-workshops@d120.de hinzugefügt werden. Nach dem Login kannst du deine(n) Workshop(s) verwalten. Solltest du irgendwelche weiteren Fragen haben melde dich einfach bei uns unter ofahrt-leitung@d120.de.\n\nMit freundlichen Grüßen,\n(okay, das ist eine automatische Mail)", "ofahrt-leitung@d120.de", [u.email])

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
                password = randomword(15)
                u = User.objects.create_user(username, user.email, password)
                u.first_name = user.first_name
                u.last_name = user.last_name
                u.is_staff = True
                u.is_active = True
                u.save()
                for group in user.orga_for.all():
                    u.groups.add(group)
                user.delete()
                send_mail("Willkommen im Orgateam der Ofahrt!", "Hallo " + user.first_name +",\n\nwillkommen im Orgateam der Ofahrt! Mit dem Erhalt dieser Email wurde den Account in pyofahrt, unserem Verwaltungstool zur Planung uns Strukturierung der OFahrt, freigeschaltet. Im folgenden findest du deine Logindaten.\n\npyofahrt: http://d120.de/ofahrt\nName: " + username + "\nPasswort: " + password + "\n\nIm Adminmenü kannst du dein Passwort jederzeit ändern. Du solltest desweiteren zeitnah auf unsere Orgaliste ofahrt@d120.de hinzugefügt werden. Solltest du irgendwelche weiteren Fragen haben melde dich einfach bei uns unter ofahrt-leitung@d120.de.\n\nMit freundlichen Grüßen,\n(okay, das ist eine automatische Mail)", "ofahrt-leitung@d120.de", [u.email])

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
