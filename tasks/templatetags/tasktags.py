from django import template
from tasks.models import Task

register = template.Library()


@register.simple_tag
def user_tasks(user):
    return Task.objects.all().filter(status="zugewiesen").filter(editors=user)

@register.assignment_tag(takes_context=True)
def user_tasks_counter(context, user):
    return Task.objects.all().filter(status="zugewiesen").filter(editors=user).count()
