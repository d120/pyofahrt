from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import Group

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

from staff.models import OrgaCandidate, WorkshopCandidate
from ofahrtbase.models import Setting, Ofahrt
from staff.forms import ContactForm



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
        send_mail("Betreff", "Nachricht", "chris.wars@yahoo.de", ["cjanuschkowetz@d120.de"])
        return super(ContactView, self).form_valid(form)




class SuccessView(TemplateView):
    template_name = "staff/success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open")
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context



class SignUpWorkshopView(CreateView):
    model = WorkshopCandidate
    template_name = "staff/signup_workshop.html"
    success_url = "/staff/signup/success/"

    fields = ['first_name', 'last_name', 'email', 'phone', 'workshop_ideas']



    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()
        return super(SignUpWorkshopView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpWorkshopView, self).get_context_data(**kwargs)
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context


class SignUpOrgaView(CreateView):
    model = OrgaCandidate

    template_name = "staff/signup_orga.html"
    success_url = "/staff/signup/success/"

    fields = ['first_name', 'last_name', 'email', 'phone', 'orga_for']



    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()
        return super(SignUpOrgaView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpOrgaView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open") and not (Group.objects.exclude(permissions__codename = "group_full").count() == 0)
        return context
