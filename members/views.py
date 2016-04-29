from django.views.generic import CreateView, TemplateView
from members.models import Member
from ofahrtbase.models import Ofahrt, Setting
from django.core.mail import send_mail


class SignUpView(CreateView):
    template_name = "members/signup.html"
    success_url = "/members/success/"
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'email', 'birth_date', 'food_preference', 'food_handicaps', 'free_text']
    success_url = "/members/success/"

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()
        send_mail("Anmeldung zur Ofahrt im Wintersemester " + str(member.base.begin_date.year), "Hallo " + member.first_name + ",\n\nwir haben deine Anmeldung für die Ofahrt für Bachelor-Erstsemester im WiSe " + str(member.base.begin_date.year) + " erfolgreich gespeichert.\nBis zum Eingang des Teilnahmebetrags von 10€ stehst du lediglich auf der vorläufigen Teilnahmeliste. Bitte überweise den Teilnahmebetrag schnellstmöglich an die unten genannten Kontodaten. Wähle als Verwendungszweck bitte \"Ofahrt Teilnahmebetrag - VORNAME NACHNAME\" damit wir die Überweisung deiner Anmeldung zuordnen können. Solltest du keinen Zugriff auf ein Bankkonto oder eine andere Möglichkeit der Überweisung haben, kontaktiere uns bitte unter ofahrt-leitung@d120.de. In diesem Fall finden wir eine Regelung für eine Barzahlung im Fachschaftsraum.\n\nSobald wir den Teilnahmebetrag erhalten haben setzen wir dich schnellstmöglich auf die feste Teilnahmeliste. Alle weiteren Infos erhälst du dann per Email.\n\nLiebe Grüße,\n die Ofahrt-Leitung\n\n-------------------------------\n\nKontodaten:\nFOLGT", "ofahrt-leitung@d120.de", [member.email])
        return super(SignUpView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["member_reg_open"] = Setting.get_Setting("member_reg_open")
        return context


class SuccessView(TemplateView):
    template_name = "members/success.html"


class MemberlistView(TemplateView):
    template_name = "members/memberlist.html"

    def get_context_data(self, **kwargs):
        context = super(MemberlistView, self).get_context_data(**kwargs)
        context["members_cond"] = Member.objects.filter(money_received = False)
        context["members_fin"] = Member.objects.filter(money_received = True)
        return context
