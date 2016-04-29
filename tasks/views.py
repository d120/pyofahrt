from django.shortcuts import render, redirect, get_object_or_404
from .models import TaskCategory, Task, TaskComment, TaskHistoryEntry
from django.views.generic.base import TemplateView, RedirectView
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

class OverviewView(TemplateView):
    template_name = "tasks/overview.html"

    def get_context_data(self, **kwargs):
        context = super(OverviewView, self).get_context_data(**kwargs)
        context["cats"] = TaskCategory.objects.all().filter(access_for__in=self.request.user.groups.all()).distinct()
        return context



class TicketEditView(UpdateView):
    model=Task
    fields = ["name", "category", "priority", "description"]
    template_name = "tasks/editticket.html"

    def get_success_url(self):
        entry = TaskHistoryEntry()
        entry.ticket = self.object
        entry.user = self.request.user
        entry.timestamp = datetime.now()
        entry.text = "<b>Ticket bearbeitet:</b> Ticket #"
        entry.save()
        return reverse('tasks:showticket', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(TicketEditView, self).get_context_data(**kwargs)
        context["form"].fields["category"].queryset = TaskCategory.objects.all().filter(access_for__in=self.request.user.groups.all()).distinct()
        return context


class TicketAssignView(UpdateView):
    model=Task
    fields = ["editors"]
    template_name = "tasks/assign.html"


    def get_success_url(self):
        entry = TaskHistoryEntry()
        entry.ticket = self.object
        entry.user = self.request.user
        entry.timestamp = datetime.now()
        editorlist = []
        for x in self.object.editors.all():
            editorlist.append(str(x))
        if not editorlist:
            editorlist.append("<i>-niemand-</i>")
            if self.object.status == "zugewiesen":
                entry.ticket.status = "neu"
                subentry = TaskHistoryEntry()
                subentry.ticket = self.object
                subentry.user = self.request.user
                subentry.timestamp = datetime.now()
                subentry.text = "<b>Status geändert:</b> neu"
                subentry.save()
        else:
            if self.object.status == "neu":
                entry.ticket.status = "zugewiesen"
                subentry = TaskHistoryEntry()
                subentry.ticket = self.object
                subentry.user = self.request.user
                subentry.timestamp = datetime.now()
                subentry.text = "<b>Status geändert:</b> zugewiesen"
                subentry.save()

        entry.text = "<b>Ticketzuweisung geändert:</b> Bearbeiter gesetzt auf " + ", ".join(editorlist)
        entry.save()
        entry.ticket.updated_at = datetime.now()
        entry.ticket.save()
        return reverse('tasks:showticket', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(TicketAssignView, self).get_context_data(**kwargs)
        return context



def push(request, ticket):
    if Task.objects.filter(id=ticket).count() == 0:
        raise Http404("Ticket existiert nicht")
    else:
        element = Task.objects.get(id=ticket)
        if request.user.is_authenticated():
            element.updated_at = datetime.now()
            element.save()

            entry = TaskHistoryEntry()
            entry.user = request.user
            entry.timestamp = datetime.now()
            entry.ticket = element
            entry.text = "<b>Push!</b>"
            entry.save()
    return HttpResponseRedirect(reverse("tasks:showticket", args=[ticket]))


def close(request, ticket):
    if Task.objects.filter(id=ticket).count() == 0:
        raise Http404("Ticket existiert nicht")
    else:
        element = Task.objects.get(id=ticket)
        if request.user.is_authenticated():
            element.status = "abgebrochen"
            element.updated_at = datetime.now()
            element.save()

            entry = TaskHistoryEntry()
            entry.user = request.user
            entry.timestamp = datetime.now()
            entry.ticket = element
            entry.text = "<b>Status geändert:</b> geschlossen"
            entry.save()
    return HttpResponseRedirect(reverse("tasks:showticket", args=[ticket]))

def finish(request, ticket):
    if Task.objects.filter(id=ticket).count() == 0:
        raise Http404("Ticket existiert nicht")
    else:
        element = Task.objects.get(id=ticket)
        if request.user.is_authenticated():
            element.status = "erledigt"
            element.updated_at = datetime.now()
            element.save()

            entry = TaskHistoryEntry()
            entry.user = request.user
            entry.timestamp = datetime.now()
            entry.ticket = element
            entry.text = "<b>Status geändert:</b> erledigt"
            entry.save()
    return HttpResponseRedirect(reverse("tasks:showticket", args=[ticket]))

def reopen(request, ticket):
    if Task.objects.filter(id=ticket).count() == 0:
        raise Http404("Ticket existiert nicht")
    else:
        element = Task.objects.get(id=ticket)
        if request.user.is_authenticated():
            #Neuen Status berechnen, abhängig davon ob es Bearbeiter gibt
            if element.editors.count() == 0:
                new_status = "neu"
            else:
                new_status = "zugewiesen"

            element.status = new_status
            element.updated_at = datetime.now()
            element.save()

            entry = TaskHistoryEntry()
            entry.user = request.user
            entry.timestamp = datetime.now()
            entry.ticket = element
            entry.text = "<b>Status geändert:</b> " + new_status + " (wiedereröffnet)"
            entry.save()
    return HttpResponseRedirect(reverse("tasks:showticket", args=[ticket]))


class TicketView(DetailView):
    model = Task
    template_name = "tasks/showticket.html"

    def get_context_data(self, **kwargs):
        context = super(TicketView, self).get_context_data(**kwargs)
        return context

class CommentView(CreateView):
    template_name = "tasks/comment.html"
    model = TaskComment
    fields = ["text"]


    def get_success_url(self):
        entry = TaskHistoryEntry()
        entry.ticket = self.object.ticket
        entry.user = self.object.user
        entry.timestamp = self.object.timestamp
        entry.text = "<b>Kommentar hinzugefügt:</b> Kommentar #" + str(self.object.id)
        entry.save()

        return reverse('tasks:showticket', args=(self.object.ticket.id,))

    def get_context_data(self, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        if Task.objects.filter(id=self.kwargs['ticket']).count() == 0:
            raise Http404("Ticket existiert nicht")
        else:
            context["ticket"] = Task.objects.get(id=self.kwargs['ticket'])
        return context

    def form_valid(self, obj):
        obj.instance.timestamp = datetime.now()
        obj.instance.ticket = Task.objects.get(id=self.kwargs['ticket'])
        obj.instance.user = self.request.user
        obj.instance.ticket.updated_at = datetime.now()
        obj.instance.ticket.save()
        return super(CommentView, self).form_valid(obj)


class TicketCreateView(CreateView):
    template_name = "tasks/create.html"
    model = Task
    fields = ["name", "category", "priority", "description"]


    def get_success_url(self):
        entry = TaskHistoryEntry()
        entry.ticket = self.object.ticket
        entry.user = self.object.user
        entry.timestamp = self.object.timestamp
        entry.text = "<b>Kommentar hinzugefügt:</b> Kommentar #" + str(self.object.id)
        entry.save()

        return reverse('tasks:showticket', args=(self.object.ticket.id,))

    def get_initial(self):
        cat = get_object_or_404(TaskCategory, pk=self.kwargs.get('category'))
        return {
            'category':cat,
        }

    def get_context_data(self, **kwargs):
        context = super(TicketCreateView, self).get_context_data(**kwargs)
        context["form"].fields["category"].queryset = TaskCategory.objects.all().filter(access_for__in=self.request.user.groups.all()).distinct()
        return context