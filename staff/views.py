from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group, User

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

from staff.models import OrgaCandidate, WorkshopCandidate
from workshops.models import Workshop
from ofahrtbase.models import Setting, Ofahrt
from staff.forms import ContactForm
from pyofahrt import settings



# Create your views here.

class SignUpView(TemplateView):
    template_name = "staff/signup.html"

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open")
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context



class ContactView(FormView):
    template_name = "staff/contact.html"
    form_class = ContactForm
    success_url = "/staff/success"

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        text = form.cleaned_data.get('message')

        mail = EmailMessage()
        mail.subject = settings.MAIL_CONTACTFORM_SUBJECT
        mail.body = settings.MAIL_CONTACTFORM_SUBJECT % {'sender' : email, 'text' : text}
        mail.to = [settings.SERVER_EMAIL]
        mail.send()

        return super(ContactView, self).form_valid(form)




class SuccessView(TemplateView):
    template_name = "staff/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open")
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context




class CreateSuperuserView(TemplateView):
    template_name = "staff/createsuperuser.html"

    def get_context_data(self, **kwargs):
        context = super(CreateSuperuserView, self).get_context_data(**kwargs)
        if User.objects.all().filter(username="leitung").count() == 0:
            User.objects.create_superuser("leitung", "ofahrt-leitung@d120.de", settings.SUPER_PASSWORD)

            mail = EmailMessage()
            mail.subject = settings.MAIL_SUPERUSER_SUCCESS_SUBJECT
            mail.body = settings.MAIL_SUPERUSER_SUCCESS_TEXT
            mail.to = ["ofahrt-leitung@d120.de"]
            mail.send()

            context["success"] = True
        else:
            User.objects.all().filter(username="leitung")[0].set_password(settings.SUPER_PASSWORD)


            mail = EmailMessage()
            mail.subject = settings.MAIL_SUPERUSER_ERROR_SUBJECT
            mail.body = settings.MAIL_SUPERUSER_ERROR_TEXT
            mail.to = ["ofahrt-leitung@d120.de"]
            mail.send()
            context["success"] = False
        return context




class SignUpWorkshopView(CreateView):
    model = WorkshopCandidate
    template_name = "staff/signup_workshop.html"
    success_url = "/staff/signup/success"

    fields = ['first_name', 'last_name', 'email', 'phone', 'workshop_ideas']

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()

        mail = EmailMessage()
        mail.subject = settings.MAIL_NEW_WORKSHOP_SUBJECT
        mail.body = settings.MAIL_NEW_WORKSHOP_TEXT % {'firstname' : member.first_name, 'lastname' : member.last_name}
        mail.to = [settings.SERVER_EMAIL]
        mail.send()

        return super(SignUpWorkshopView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpWorkshopView, self).get_context_data(**kwargs)
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        context["workshop_ideas"] = Workshop.objects.all().filter(host=None)
        return context


class SignUpOrgaView(CreateView):
    model = OrgaCandidate

    template_name = "staff/signup_orga.html"
    success_url = "/staff/signup/success"

    fields = ['first_name', 'last_name', 'email', 'phone', 'orga_for']



    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()

        mail = EmailMessage()
        mail.subject = settings.MAIL_NEW_ORGA_SUBJECT
        mail.body = settings.MAIL_NEW_ORGA_TEXT % {'firstname' : member.first_name, 'lastname' : member.last_name}
        mail.to = [settings.SERVER_EMAIL]
        mail.send()


        return super(SignUpOrgaView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpOrgaView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open") and not (Group.objects.exclude(permissions__codename = "group_full").count() == 0)
        return context
