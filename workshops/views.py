from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.views.generic import DetailView
from .models import Workshop
from ofahrtbase.models import Ofahrt
from django.contrib.auth.models import User, Group

# Create your views here.

class OverviewView(TemplateView):
    template_name = "workshops/overview.html"

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context["workshops"] = Workshop.objects.all()
        context["myworkshops"] = Workshop.objects.all().filter(host=self.request.user)
        return context


class WorkshopView(DetailView):
    template_name = "workshops/showworkshop.html"
    model = Workshop

    def get_context_data(self, **kwargs):
        context = super(WorkshopView, self).get_context_data(**kwargs)
        return context


class WorkshopEditView(UpdateView):
    template_name = "workshops/editworkshop.html"
    model = Workshop
    fields = ["description", "requirements", "conditions"]

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
    fields = ["name", "description", "requirements", "conditions"]

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
    fields = ["host"]

    def get_success_url(self):
        return reverse('workshops:show', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(WorkshopAssignView, self).get_context_data(**kwargs)
        context["form"].fields["host"].queryset = User.objects.all().exclude(groups=None)
        return context
