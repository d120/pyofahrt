from django.db import models
from datetime import datetime, timedelta, date
from ofahrtbase.models import Ofahrt, Room

# Create your models here.

class FoodHandicaps(models.Model):
    class Meta:
        verbose_name = "Lebensmittelunverträglichkeit"
        verbose_name_plural = "Lebensmittelunverträglichkeiten"

    text = models.CharField("Lebensmittelunverträglichkeit", max_length=50)

    def __str__(self):
        return self.text


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

    FOOD_PREFERENCE_CHOICES = (
        ("normal", "nein"),
        ("vegetarisch", "Vegetarisch"),
        ("vegan", "Vegan")
    )

    first_name = models.CharField("Vorname", max_length=30)
    last_name = models.CharField("Nachname", max_length=30)
    gender = models.CharField("Geschlecht", choices=GENDER_CHOICES, help_text="Diese Angabe wird nur für die Zuteilung der Schlafräume minderjähriger Teilnehmer verwendet.", max_length=25, default="n")

    email = models.EmailField("Emailadresse", unique=True)
    birth_date = models.DateField("Geburtsdatum")

    food_preference = models.CharField("Vegetarier?", choices=FOOD_PREFERENCE_CHOICES, max_length=30, default="normal")
    food_handicaps = models.ManyToManyField(FoodHandicaps, help_text="Um Einträge abzuwählen, die STRG-Taste gedrückt halten und Klicken.", verbose_name = "Sonstige Lebensmittelunverträglichkeiten", blank=True)

    is_really_ersti = models.BooleanField("Geprüft ob Ersti?", default=False)
    queue = models.BooleanField("Warten auf Geldeingang")
    queue_deadline = models.DateTimeField("Deadline für Geldeingang", null=True)
    money_received = models.BooleanField("Festangemeldet?", default=False)


    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Eingetragen am")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Verändert am")

    free_text = models.TextField("Sonstige Anmerkungen", blank=True)
    room = models.ForeignKey(Room, verbose_name = "Zugeteilter Raum", null=True, blank=True)


    def is_full_aged(self):
        return date.today() >= date(self.birth_date.year + 18, int(self.birth_date.month), int(self.birth_date.day) )
    is_full_aged.boolean = True
    is_full_aged.short_description = "Derzeit volljährig?"

    def get_room_for_nametag(self):
        if self.room == None:
            return "Kein Raum zugeteilt!"
        else:
            return self.room


    def __str__(self):
        return self.first_name + " " + self.last_name
