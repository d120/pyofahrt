from django.db import models
from ofahrtbase.models import Ofahrt
from django.contrib.auth.models import Group, Permission

# Create your models here.

class Candidate(models.Model):

    class Meta:
        abstract = True

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige Ofahrt")

    first_name = models.CharField("Vorname", max_length=30)
    last_name = models.CharField("Nachname", max_length=30)

    email = models.EmailField("Email-Adresse")
    phone = models.CharField("Handynummer", max_length=30)


    def __str__(self):
        return self.first_name + " " + self.last_name

from  django.db.models.query_utils import Q
class OrgaCandidate(Candidate):
    class Meta:
        verbose_name = "Orgabewerber"
        verbose_name_plural = "Orgabewerber"


    orga_for = models.ManyToManyField(Group, limit_choices_to=~Q(permissions__codename = "group_full"), verbose_name="Orgajob", help_text="Hier kannst du eine oder mehrere Orgatätigkeiten auswählen, für die du dich interessierst.")


class WorkshopCandidate(Candidate):
    class Meta:
        verbose_name = "Workshopbewerber"
        verbose_name_plural = "Workshopbewerber"

        permissions = (
            ("group_full", "Gruppe ist voll"),
        )

    workshop_ideas = models.TextField("Workshopideen", help_text='Bei mehreren Ideen, bitte eine Zeile pro Idee verwenden.')
