from django.views.generic import TemplateView
from .models import Setting, Ofahrt
from workshops.models import Slot


class WelcomeView(TemplateView):
    template_name = "ofahrtbase/welcome.html"

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['orga_reg_open'] = Setting.get_Setting("orga_reg_open")
        context['workshop_reg_open'] = Setting.get_Setting("workshop_reg_open")
        context['ofahrt'] = Ofahrt.current()
        return context

class ScheduleView(TemplateView):
    template_name = "ofahrtbase/timetable.html"


    def get_context_data(self, **kwargs):
        #Helpers
        def datetime2moment(input):
            return str(input.year) + "-" + str(input.month) + "-" + str(input.day) + "T" + str(input.hour) + ":" + str(input.minute) + ":" + str(input.second)
        def date2moment(input):
            return str(input.year) + "-" + str(input.month) + "-" + str(input.day)

        context = super(ScheduleView, self).get_context_data(**kwargs)


        context["first"] = date2moment(Ofahrt.current().begin_date)
        context["events"] = Slot.objects.all();
        
        return context
