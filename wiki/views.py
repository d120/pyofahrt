from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect
from .models import Article, ArticleVersion
import datetime
from django.http import Http404, HttpResponseRedirect

# Create your views here.



def mainview(request):
    return HttpResponseRedirect(reverse("wiki:show", kwargs={"pk": Article(title="WikiStart")}))


class PageView(DetailView):
    model = Article
    template_name = "wiki/article.html"

    def get_object(self, queryset=None):
        out = super(PageView, self).get_object()
        out.text = out.articleversion_set.order_by('-timestamp')[:1].get().text
        return out

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context["tab"] = "view"
        return context


    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect(reverse_lazy("wiki:create", kwargs={"title": kwargs["pk"]}))
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class PageVersionView(DetailView):
    model = Article
    template_name = "wiki/article.html"

    def get_object(self, queryset=None):
        out = super(PageVersionView, self).get_object()
        try:
            out.text = out.articleversion_set.get(id=self.kwargs["id"]).text
        except ArticleVersion.DoesNotExist:
            out.text = out.articleversion_set.order_by('-timestamp')[:1].get().text
        return out

    def get_context_data(self, **kwargs):
        context = super(PageVersionView, self).get_context_data(**kwargs)
        context["tab"] = "viewhistory"
        return context


class PageHistoryView(ListView):
    model = Article
    template_name = "wiki/articlehistory.html"

    def get_queryset(request, *args, **kwargs):
        out = ArticleVersion.objects.filter(article=request.kwargs["title"])
        return out

    def get_context_data(self, **kwargs):
        context = super(PageHistoryView, self).get_context_data(**kwargs)
        context["tab"] = "history"
        context['object'] = self.kwargs["title"]
        return context


class PageCreateView(CreateView):
    model = ArticleVersion
    fields = ["text"]
    template_name = "wiki/create.html"


    def form_valid(self, form):
        try:
            article = Article.objects.get(title=self.kwargs["title"])
        except Article.DoesNotExist:
            article = Article(title = self.kwargs["title"])
            article.save()

        form.instance.article = article
        form.instance.timestamp = datetime.datetime.now()
        return super(PageCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        context["tab"] = "edit"
        context["titel"] = self.kwargs["title"]
        try:
            context["object"] = Article(title = self.kwargs["title"])
        except Article.DoesNotExist:
            pass
        return context



class PageEditView(CreateView):
    model = ArticleVersion
    fields = ["text"]
    template_name = "wiki/edit.html"


    def form_valid(self, form):
        try:
            article = Article.objects.get(title=self.kwargs["title"])
        except Article.DoesNotExist:
            return

        form.instance.article = article
        form.instance.timestamp = datetime.datetime.now()
        return super(PageEditView, self).form_valid(form)


    def get_initial(self):
        try:
            article = Article.objects.get(title=self.kwargs["title"])
        except Article.DoesNotExist:
            return
        return { 'text' : article.articleversion_set.order_by('-timestamp')[:1].get().text}

    def get_context_data(self, **kwargs):
        context = super(PageEditView, self).get_context_data(**kwargs)
        context["object"] = self.kwargs["title"]
        context["tab"] = "edit"
        return context
