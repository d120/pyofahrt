from django.contrib import admin
from workshops.models import Workshop, Slot
from workshops.admin_actions import set_accepted

germandays = {
    "0": "Montag",
    "1": "Dienstag",
    "2": "Mittwoch",
    "3": "Donnerstag",
    "4": "Freitag",
    "5": "Samstag",
    "6": "Sonntag",
}


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = [
        "name", "show_hosts", "show_slot", "room", "accepted", "proved"
    ]
    list_filter = ["host", "slot", "room", "accepted", "proved"]
    actions = [set_accepted,]

    def show_hosts(self, obj):
        return ", ".join([str(t) for t in obj.host.all()])

    show_hosts.short_description = "Anbieter"
    show_hosts.admin_order_field = 'host__username'   # making this field sortable by host's username

    def longstr(self, slot):
        return slot.name + " - " + germandays[slot.begin.strftime(
            '%w')] + " (" + slot.begin.strftime(
                '%H:%M') + " - " + slot.end.strftime('%H:%M') + ")"

    def show_slot(self, obj):
        slotname = str(obj.slot)
        slot = Slot.objects.get(name=slotname)
        return self.longstr(slot)

    show_slot.short_description = "Zeitslot"
    show_slot.admin_order_field = 'slot__begin'   # making this field sortable by time slot beginning


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["name", "begin", "end", "slottype", "priority"]
    date_hierarchy = "begin"
    ordering = ["begin"]
