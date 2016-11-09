from django.template.response import SimpleTemplateResponse
from django.template import loader
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponse
from ofahrtbase.helper import LaTeX
import datetime

from .models import Member

def mail_export(modeladmin, request, queryset):
    template = loader.get_template("admin/mail_export.html")
    context = {'persons' : queryset,
        'opts' : modeladmin.opts,
        'title' : 'Mailexport'}
    return SimpleTemplateResponse(template, context)

mail_export.short_description = "Mailexport"


def nametag_export(modeladmin, request, queryset):
    (pdf, pdflatex_output) = LaTeX.render(
        {"members": queryset, "generator": "members/nametags.tex"},
        'ofahrtbase/nametags.tex', ['weggeWesen.jpg'],
        'ofahrtbase')

    if pdf is None:
        return HttpResponse(pdflatex_output[0].decode("utf-8"))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=nametags-members.pdf'
    response.write(pdf)


    return response



nametag_export.short_description = "Namensschilder generieren"


def mark_participants_contributing_paid(modeladmin, request, queryset):
    queryset.update(money_received=True)
    modeladmin.message_user(request, "%d Teilnehmer*innen erfolgreich auf die feste Anmeldeliste gesetzt. Neue Festanmeldungen: %d" % (queryset.count(), Member.objects.filter(money_received=True).count()))

mark_participants_contributing_paid.short_description = "Schieben: temp. Liste => fest. Liste"


def move_to_queue(modeladmin, request, queryset):
    queryset.update(queue=True)
    queryset.update(queue_deadline=datetime.datetime.now() + datetime.timedelta(7))


    for member in queryset.all():
        email = EmailMessage()
        email.subject = settings.MAIL_MEMBER_MOVETOQUEUE_SUBJECT
        email.body = settings.MAIL_MEMBER_MOVETOQUEUE_TEXT % (member.first_name, settings.BANK_ACCOUNT)
        email.to = [member.email]
        email.send()



    modeladmin.message_user(request, "%d Teilnehmer*innen erfolgreich auf die vorläufige Anmeldeliste gesetzt und per Mail informiert." % queryset.count())

move_to_queue.short_description = "Schieben: Warteschlange => temp. Liste"
