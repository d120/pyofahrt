from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib.auth.models import Group, User, Permission
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.db.models import Q

from staff.models import OrgaCandidate, WorkshopCandidate
from workshops.models import Workshop
from ofahrtbase.models import Setting, Ofahrt
from staff.forms import ContactForm, PasswordForm
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
    success_url = reverse_lazy('staff:successcontact')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        text = form.cleaned_data.get('message')

        mail = EmailMessage()
        mail.subject = settings.MAIL_CONTACTFORM_SUBJECT
        mail.body = settings.MAIL_CONTACTFORM_TEXT % {'sender' : email, 'text' : text}
        mail.to = [settings.SERVER_EMAIL]
        mail.send()

        return super(ContactView, self).form_valid(form)


class PasswordView(FormView):
    template_name = "staff/changepassword/changepassword.html"
    form_class = PasswordForm
    success_url = reverse_lazy("staff:changepasswordsuccess")

    def get_form_kwargs(self):
        kwargs = super(PasswordView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.request.user.set_password(form.cleaned_data.get('newpassworda'))
        self.request.user.save()
        return super(PasswordView, self).form_valid(form)



class SuccessView(TemplateView):
    template_name = "staff/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open")
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context



class PasswordSuccessView(TemplateView):
    template_name = "staff/changepassword/success.html"



class SignUpWorkshopView(CreateView):
    model = WorkshopCandidate
    template_name = "staff/signup_workshop.html"
    success_url = reverse_lazy('staff:success')

    fields = ['first_name', 'last_name', 'email', 'phone', 'workshop_ideas']

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()

        #Adressen aller Workshoporgas erfragen
        perm = Permission.objects.get(codename='editeveryworkshop')
        orgas = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
        print(list(orgas.values_list('email', flat=True)))

        mail = EmailMessage()
        mail.subject = settings.MAIL_NEW_WORKSHOP_SUBJECT
        mail.body = settings.MAIL_NEW_WORKSHOP_TEXT % {'firstname' : member.first_name, 'lastname' : member.last_name}
        mail.to = list(orgas.values_list('email', flat=True))
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
    success_url = reverse_lazy('staff:success')

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
