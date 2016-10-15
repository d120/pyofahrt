from django.template.response import SimpleTemplateResponse
from django.template import loader

def mail_export(modeladmin, request, queryset):
    template = loader.get_template("admin/mail_export.html")
    context = {'persons' : queryset,
        'opts' : modeladmin.opts,
        'title' : 'Mailexport'}
    return SimpleTemplateResponse(template, context)

mail_export.short_description = "Mailexport"
