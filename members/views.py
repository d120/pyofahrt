from django.views.generic import CreateView, TemplateView
from members.models import Member
from ofahrtbase.models import Ofahrt, Setting
from django.core.mail import EmailMessage
from pyofahrt import settings


class SignUpView(CreateView):
    template_name = "members/signup.html"
    success_url = "/members/success"
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'email', 'birth_date', 'food_preference', 'food_handicaps', 'free_text']
    success_url = "/members/success"

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()

        email = EmailMessage()
        email.subject = settings.MAIL_MEMBERSIGNUP_SUBJECT % (member.base.begin_date.year)
        email.body = settings.MAIL_MEMBERSIGNUP_TEXT % (member.first_name, member.base.begin_date.year)
        email.to = [member.email]
        email.send()

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

        for index, member in enumerate(context["members_cond"]):
            context["members_cond"][index].last_name = member.last_name[:1] + "."

        for index, member in enumerate(context["members_fin"]):
            context["members_fin"][index].last_name = member.last_name[:1] + "."

        return context
