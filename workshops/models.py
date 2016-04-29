from django.db import models
from staff.models import WorkshopCandidate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ofahrtbase.models import Ofahrt

# Create your models here.


class Slot(models.Model):
    class Meta:
        verbose_name = "Zeitslot"
        verbose_name_plural = "Zeitslots"


    name = models.CharField("Bezeichnung", max_length=30, unique=True)
    begin = models.DateTimeField("Start")
    end = models.DateTimeField("Ende")

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

    def clean(self):
        if self.begin > self.end:
            raise ValidationError("Der Startzeitpunkt muss vor dem Entzeitpunkt liegen")


class Workshop(models.Model):
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige Ofahrt")

    name = models.CharField("Titel", max_length=50)
    description = models.TextField("Beschreibung", blank=True)
    host = models.ManyToManyField(User, verbose_name="Workshopanbieter")

    slot = models.ForeignKey(Slot, verbose_name="Zugeteilter Zeitslot", null=True, blank=True)
