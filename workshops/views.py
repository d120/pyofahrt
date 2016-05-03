from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import DetailView
from .models import Workshop

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
