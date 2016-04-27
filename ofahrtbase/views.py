from django.views.generic import TemplateView
from .models import Setting, Ofahrt


class WelcomeView(TemplateView):
    template_name = "ofahrtbase/welcome.html"

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['orga_reg_open'] = Setting.get_Setting("orga_reg_open")
        context['workshop_reg_open'] = Setting.get_Setting("workshop_reg_open")
        context['ofahrt'] = Ofahrt.current()
        return context


class ScheduleView(TemplateView):
    template_name = "ofahrtbase/freetext.html"

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['text'] = "Coming soon ;-)"
        return context
