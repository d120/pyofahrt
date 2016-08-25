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
        context = super(ScheduleView, self).get_context_data(**kwargs)

        slots = Slot.objects.all().order_by("begin")
        days = set()
        steps = set()

        weekdays = {}
        weekdays[0] = "Montag"
        weekdays[1] = "Dienstag"
        weekdays[2] = "Mittwoch"
        weekdays[3] = "Donnerstag"
        weekdays[4] = "Freitag"
        weekdays[5] = "Samstag"
        weekdays[6] = "Sonntag"


        for slot in slots:
            weekday = slot.begin.weekday()
            starthour = slot.begin.hour
            days.add(weekday)
            steps.add(starthour)

        stepdiff = (max(steps) - min(steps)) + 1

        # Matrix generieren (+1 für Metazellen oben und links)
        out = [["" for x in range(len(days) + 1)] for y in range(stepdiff + 1)]


        #Kopfzeile oben
        i = 1
        out[0][0] = "Zeiten"
        for x in days:
            out[0][i] = weekdays[x]
            i += 1

        #Kopfzeile links (Zeiten)
        i = 1
        for x in range(min(steps), max(steps)+1):
            out[i][0] = str(x) + ":00"
            i += 1


        #Inhalte laden
        for zeile, zeilewert in enumerate(out[1:]):
            for spalte, spaltewert in enumerate(out[zeile][1:]):
                out[zeile+1][spalte+1] = str(zeile) + "/" + str(spalte)




        print(days)
        context["timetable"] = out

        return context
