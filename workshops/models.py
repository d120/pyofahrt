from django.db import models
from staff.models import WorkshopCandidate

# Create your models here.

class Workshop(models.Model):
    name = models.CharField("Titel", max_length=50)
    description = models.TextField("Beschreibung", blank=True)
