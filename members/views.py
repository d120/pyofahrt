from django.views.generic import CreateView, TemplateView
from members.models import Member
from ofahrtbase.models import Ofahrt, Setting


class SignUpView(CreateView):
    template_name = "members/signup.html"
    success_url = "/members/success/"
    model = Member
    fields = ['first_name', 'last_name', 'gender', 'email', 'birth_date']
    success_url = "/members/success/"

    def form_valid(self, form):
        member = form.save(commit=False)
        member.base = Ofahrt.current()
        return super(SignUpView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context["member_reg_open"] = Setting.get_Setting("member_reg_open")
        return context


class SuccessView(TemplateView):
    template_name = "members/success.html"

class MemberlistView(TemplateView):
    template_name = "ofahrtbase/freetext.html"

    def get_context_data(self, **kwargs):
        context = super(MemberlistView, self).get_context_data(**kwargs)
        context['text'] = "Coming soon ;-)"
        return context
