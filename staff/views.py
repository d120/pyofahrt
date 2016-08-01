from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib.auth.models import Group, User

from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView

from staff.models import OrgaCandidate, WorkshopCandidate
from ofahrtbase.models import Setting, Ofahrt
from staff.forms import ContactForm
from pyofahrt.settings import SUPER_PASSWORD



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
        mail = form.cleaned_data.get('email')
        text = form.cleaned_data.get('message')

        send_mail("Ofahrt Kontaktformular", "Ofahrt Kontaktformular (Anfrage von " + mail + ")\n\n\n" + text, "noreply@d120.de", ["ofahrt-leitung@d120.de"])
        print()
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
            User.objects.create_superuser("leitung", "ofahrt-leitung@d120.de", SUPER_PASSWORD)
            send_mail("SuperUser neu angelegt", "Der Superuseraccount \"leitung\" wurde in pyofahrt neu angelegt. Die Zugangsdaten findest du unter mnt/media/ofahrt/pw.txt", "noreply@d120.de", ["ofahrt-leitung@d120.de"])
            context["success"] = True
        else:
            User.objects.all().filter(username="leitung")[0].set_password(SUPER_PASSWORD)
            send_mail("SuperUser konnte nicht neu angelegt werden", "Es wurde beantragt den Superuseraccount \"leitung\" in pyofahrt neu anzulegen. Da der Account allerdings nicht gelöscht wurde, wurde das Passwort zurückgesetzt. Die Zugangsdaten findest du unter mnt/media/ofahrt/pw.txt", "noreply@d120.de", ["ofahrt-leitung@d120.de"])
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
        send_mail("pyofahrt: Neuer Workshop-Eintrag", "Eine neue Workshop-Bewerbung ist eingegangen. Bitte zeitnah bearbeiten.\n\nVorname: " + member.first_name + "\nNachname: " + member.last_name, "ofahrt-leitung@d120.de", ["ofahrt-leitung@d120.de"])
        return super(SignUpWorkshopView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpWorkshopView, self).get_context_data(**kwargs)
        context["workshop_reg_open"] = Setting.get_Setting("workshop_reg_open")
        return context


class SignUpOrgaView(CreateView):
    model = OrgaCandidate

    template_name = "staff/signup_orga.html"
    success_url = "/staff/signup/success"

    fields = ['first_name', 'last_name', 'email', 'phone', 'orga_for']



    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()
        send_mail("pyofahrt: Neuer Orga-Eintrag", "Eine neue Orga-Bewerbung ist eingegangen. Bitte zeitnah bearbeiten.\n\nVorname: " + member.first_name + "\nNachname: " + member.last_name, "ofahrt-leitung@d120.de", ["ofahrt-leitung@d120.de"])
        return super(SignUpOrgaView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpOrgaView, self).get_context_data(**kwargs)
        context["orga_reg_open"] = Setting.get_Setting("orga_reg_open") and not (Group.objects.exclude(permissions__codename = "group_full").count() == 0)
        return context
