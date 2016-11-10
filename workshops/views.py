from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from django.views.generic import DetailView
from .models import Workshop, Slot
from .forms import DuplicateForm
from ofahrtbase.models import Ofahrt, Room
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from ofahrtbase.helper import LaTeX

# Create your views here.

class OverviewView(TemplateView):
    template_name = "workshops/overview.html"

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context["workshops"] = Workshop.objects.all().exclude(host=None)
        context["myworkshops"] = Workshop.objects.all().filter(host=self.request.user)
        context["newworkshops"] = Workshop.objects.all().filter(host=None)
        return context


class WorkshopDuplicateView(FormView):
    template_name = "workshops/duplicateworkshop.html"
    form_class = DuplicateForm
    success_url = reverse_lazy("workshops:overview")

    def get_context_data(self, **kwargs):
        context = super(WorkshopDuplicateView, self).get_context_data(**kwargs)
        context["object"] = Workshop.objects.get(pk=self.kwargs["pk"])
        return context

    def form_valid(self, form):
        original = Workshop.objects.get(pk=self.kwargs["pk"])
        original.pk = None
        original.slot = form.cleaned_data.get('slot')
        original.save()
        return super(WorkshopDuplicateView, self).form_valid(form)



class WorkshopView(DetailView):
    template_name = "workshops/showworkshop.html"
    model = Workshop

    def get_context_data(self, **kwargs):
        context = super(WorkshopView, self).get_context_data(**kwargs)
        return context



class WorkshopTakeView(DetailView):
    template_name = "workshops/takeworkshop.html"
    model = Workshop

    def get_context_data(self, **kwargs):
        context = super(WorkshopTakeView, self).get_context_data(**kwargs)
        return context

def takeit(request, pk):
    if Workshop.objects.filter(id=pk).count() == 0:
        raise Http404("Ticket existiert nicht")
    else:
        element = Workshop.objects.get(id=pk)
        if request.user.is_authenticated():
            element.host.add(request.user)
            element.save()
    return HttpResponseRedirect(reverse("workshops:show", args=[pk]))


class WorkshopEditView(UpdateView):
    template_name = "workshops/editworkshop.html"
    model = Workshop
    fields = ["description", "requirements", "conditions", "maxmembers"]

    def get_context_data(self, **kwargs):
        context = super(WorkshopEditView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('workshops:show', args=(self.object.id,))


class WorkshopDeleteView(DeleteView):
    template_name = "workshops/deleteworkshop.html"
    model = Workshop

    def get_context_data(self, **kwargs):
        context = super(WorkshopDeleteView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('workshops:overview')

class WorkshopCreateView(CreateView):
    template_name = "workshops/createworkshop.html"
    model = Workshop
    fields = ["name", "description", "requirements", "conditions", "maxmembers", "otherstuff"]

    def get_context_data(self, **kwargs):
        context = super(WorkshopCreateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        self.object.host = [self.request.user]
        self.object.save()
        return reverse('workshops:show', args=(self.object.id,))

    def form_valid(self, form):
        form.instance.base = Ofahrt.current()
        return super(WorkshopCreateView, self).form_valid(form)



class WorkshopAssignView(UpdateView):
    template_name = "workshops/assignworkshop.html"
    model = Workshop
    fields = ["host", "room"]

    def get_success_url(self):
        return reverse('workshops:show', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(WorkshopAssignView, self).get_context_data(**kwargs)
        context["form"].fields["host"].queryset = User.objects.all().exclude(groups=None)
        context["form"].fields["room"].queryset = Room.objects.all().filter(usecase_workshop=True)
        return context


class WorkshopPlanView(TemplateView):
    template_name = "workshops/planer.html"

    def get_context_data(self, **kwargs):
        context = super(WorkshopPlanView, self).get_context_data(**kwargs)
        context["rooms"] = Room.objects.all().filter(usecase_workshop=True).order_by("number")
        context["slots"] = Slot.objects.all().filter(slottype="workshop").order_by("begin")
        context["workshops"] = Workshop.objects.all()
        return context



def saveworkshopassignment(request):
    results = {'success': False}
    if request.method == u'GET':
        GET = request.GET

        slotid = int(GET['slot'])
        roomid = int(GET['room'])
        workshopid = int(GET['workshop'])

        try:
            workshop = Workshop.objects.get(pk=workshopid)
            room = None if roomid == 0 else Room.objects.get(pk=roomid)
            slot = None if slotid == 0 else Slot.objects.get(pk=slotid)
        except (Workshop.DoesNotExist, Room.DoesNotExist, Slot.DoesNotExist):
            return HttpResponse(results)

        workshop.room = room
        workshop.slot = slot

        workshop.save()
        results = {'success': True}
    return HttpResponse(results)

def infoexport(request):
    queryset = Workshop.objects.all().filter(accepted=True).filter(proved=True)
    (pdf, pdflatex_output) = LaTeX.render(
        {"workshops": queryset},
        'workshops/ofahrtheft.tex', ['grafik/logo_ohne_rand.png', 'grafik/titel.png', 'grafik/umgebung_big.png', 'grafik/umgebung_small.png', 'inhalt/einleitung.tex', 'inhalt/rueckseite.tex', 'inhalt/titelseite.tex', 'paket/ofahrtheft.sty'],
        'workshops')

    if pdf is None:
        return HttpResponse(pdflatex_output[0].decode("utf-8"))

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=infoheft.pdf'
    response.write(pdf)

    return response