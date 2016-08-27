from django.contrib import admin
from workshops.models import Workshop, Slot

germandays = {
"0" : "Montag",
"1" : "Dienstag",
"2" : "Mittwoch",
"3" : "Donnerstag",
"4" : "Freitag",
"5" : "Samstag",
"6" : "Sonntag",
}


# Register your models here.

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ["name", "show_hosts", "show_slot", "accepted", "proved"]
    list_filter = ["host", "slot", "accepted", "proved"]

    def show_hosts(self, obj):
        return ", ".join([str(t) for t in obj.host.all()])
    show_hosts.short_description = "Anbieter"

    def longstr(self, slot):
        return slot.name + " - " + germandays[slot.begin.strftime('%w')] + " (" + slot.begin.strftime('%H:%M') + " - " + slot.end.strftime('%H:%M') + ")"

    def show_slot(self, obj):
        slotname = str(obj.slot)
        slot = Slot.objects.get(name=slotname)
        return self.longstr(slot)
    show_slot.short_description = "Zeitslot"



@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ["name", "begin", "end", "slottype", "priority"]
    date_hierarchy = "begin"
    ordering = ["begin"]
