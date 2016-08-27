from django.db import models
from staff.models import WorkshopCandidate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ofahrtbase.models import Ofahrt
from datetime import datetime

# Create your models here.


class Slot(models.Model):
    class Meta:
        verbose_name = "Zeitslot"
        verbose_name_plural = "Zeitslots"


    name = models.CharField("Bezeichnung", max_length=30)
    begin = models.DateTimeField("Start", default=datetime.combine(Ofahrt.current().begin_date, datetime.min.time()))
    end = models.DateTimeField("Ende", default=datetime.combine(Ofahrt.current().begin_date, datetime.min.time()))

    SLOT_CHOICES = (
        ("workshop", "Workshop"),
        ("event", "Zentrale Veranstaltung"),
        ("food", "Essen"),
        ("sonstiges", "Sonstiges")
    )

    PRIORITY_CHOICES = (
        ("opt", "optional"),
        ("zentral", "zentral"),
        ("dezentral", "dezentral"),
        ("wichtig", "wichtig")
    )

    slottype = models.CharField("Art des Slots", choices=SLOT_CHOICES, max_length=30, default="sonstiges")
    priority = models.CharField("Priorität", choices=PRIORITY_CHOICES, max_length=30, default="zentral")


    def __str__(self):
        return self.name

    def begin_moment(self):
        return self.begin.strftime("%Y-%m-%dT%H:%M:%S")

    def end_moment(self):
        return self.end.strftime("%Y-%m-%dT%H:%M:%S")

    def calendarcolor(self):
        if self.slottype == "workshop":
            return "blue"
        elif self.slottype == "event":
            return "red"
        elif self.slottype == "food":
            return "green"
        else:
            return "grey"

    def clean(self):
        if self.begin > self.end:
            raise ValidationError("Der Startzeitpunkt muss vor dem Entzeitpunkt liegen")


class Workshop(models.Model):
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
        permissions = (
            ("can_use", "Die Workshopkomponente nutzen"),
            ("editeveryworkshop", "Jeden Workshop bearbeiten"),
            ("proveworkshop", "Einen Workshop als geprüft markieren"),
            ("acceptworkshop", "Einen Workshop als akzeptiert markieren"),
            ("assignworkshop", "Workshopzuweisung ändern")
        )

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige Ofahrt")

    name = models.CharField("Titel", max_length=50)
    description = models.TextField("Beschreibung", blank=True)
    requirements = models.TextField("Materialbedarf", blank=True)
    conditions = models.TextField("Teilnahmebedingungen", blank=True)
    host = models.ManyToManyField(User, verbose_name="Workshopanbieter", blank=True)

    accepted = models.BooleanField("Akzeptiert", help_text="Workshopidee ist in Ordnung", default=False)
    proved = models.BooleanField("Geprüft", help_text="Der aktuelle Workshopstand ist durch den Workshoporga geprüft.", default=False)

    slot = models.ForeignKey(Slot, verbose_name="Zugeteilter Zeitslot", null=True, blank=True)

    def __str__(self):
        return self.name
