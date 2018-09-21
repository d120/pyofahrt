from django.views.generic import TemplateView
from .models import Ofahrt
from workshops.models import Slot


class WelcomeView(TemplateView):
    template_name = "ofahrtbase/welcome.html"

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['ofahrt'] = Ofahrt.current()
        return context


class ScheduleView(TemplateView):
    template_name = "ofahrtbase/timetable.html"

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)

        context["first"] = Ofahrt.current().begin_date.isoformat()
        context["events"] = Slot.objects.all()

        return context
