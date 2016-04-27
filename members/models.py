from django.db import models
from datetime import datetime, timedelta, date
from ofahrtbase.models import Ofahrt, Room

# Create your models here.
class Member(models.Model):
    class Meta:
        verbose_name = "Teilnehmer"
        verbose_name_plural = "Teilnehmer"
        unique_together = ("first_name", "last_name")

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige Ofahrt")

    GENDER_CHOICES = (
        ("m", "männlich"),
        ("w", "weiblich"),
        ("n", "keines der genannten")
    )

    first_name = models.CharField("Vorname", max_length=30)
    last_name = models.CharField("Nachname", max_length=30)
    gender = models.CharField("Geschlecht", choices=GENDER_CHOICES, help_text="Diese Angabe wird nur für die Zuteilung der Schlafräume minderjähriger Teilnehmer verwendet.", max_length=25, default="n")

    email = models.EmailField("Emailadresse", unique=True)
    birth_date = models.DateField("Geburtsdatum")

    is_really_ersti = models.BooleanField("Geprüft ob Ersti?", default=False)
    money_received = models.BooleanField("Geld eingegangen?", default=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eingetragen am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Verändert am")


    def is_full_aged(self):
        return date.today() >= date(self.birth_date.year + 18, int(self.birth_date.month), int(self.birth_date.day) )
    is_full_aged.boolean = True
    is_full_aged.short_description = "Volljährig?"


    def __str__(self):
        return self.first_name + " " + self.last_name


class RoomAssignment(models.Model):
    class Meta:
        verbose_name = "Raumzuteilung"
        verbose_name_plural = "Raumzuteilungen"
        unique_together = ("base", "room")

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige Ofahrt")

    room = models.ForeignKey(Room, verbose_name="Zugehöriger Raum")
    members = models.ManyToManyField(Member, verbose_name="Zugewiesene Personen")

    def __str__(self):
        return self.room.name
