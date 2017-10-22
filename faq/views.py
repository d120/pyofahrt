from django.shortcuts import render
from django.views.generic.base import TemplateView
from faq.models import FaqCategory, Question
import bbcode


class FaqView(TemplateView):
    template_name = "faq/overview.html"

    def get_context_data(self, **kwargs):
        context = super(FaqView, self).get_context_data(**kwargs)
        context["categories"] = FaqCategory.objects.all()

        return context
