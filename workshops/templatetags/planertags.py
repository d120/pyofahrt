from django import template

register = template.Library()


@register.simple_tag
def check_for_conflict(workshop):
    """ Counts the number of workshops in a given slot for every host in a given set of hosts.
    Returns "conflict" if it counts more than one workshop, an empty string otherwise. """
    hosts = workshop.host.all()
    slot = workshop.slot
    for host in hosts:
        if slot is not None and host.workshop_set.filter(slot=slot).count() > 1:
            return "conflict"
    return ""
