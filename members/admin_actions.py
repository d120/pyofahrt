from django.template.response import SimpleTemplateResponse
from django.template import loader

from .models import Member

def mail_export(modeladmin, request, queryset):
    template = loader.get_template("admin/mail_export.html")
    context = {'persons' : queryset,
        'opts' : modeladmin.opts,
        'title' : 'Mailexport'}
    return SimpleTemplateResponse(template, context)

mail_export.short_description = "Mailexport"


def mark_participants_contributing_paid(modeladmin, request, queryset):
    queryset.update(money_received=True)
    modeladmin.message_user(request, "%d Teilnehmer*innen erfolgreich auf die feste Anmeldeliste gesetzt. Neue Festanmeldungen: %d" % (queryset.count(), Member.objects.filter(money_received=True).count()))

mark_participants_contributing_paid.short_description = "Teilnehmerbeitrag eingegangen"
