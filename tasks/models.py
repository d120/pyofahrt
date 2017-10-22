from django.db import models
from django.contrib.auth.models import User, Group
from ofahrtbase.models import Ofahrt

# Create your models here.


class TaskCategory(models.Model):
    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorien"

    name = models.CharField("Aufgabe", max_length=255)
    description = models.TextField("Beschreibung", blank=True)
    access_for = models.ManyToManyField(
        Group, verbose_name="Zugang für", blank=True)
    responsible_for = models.ManyToManyField(
        Group,
        verbose_name="Hauptzuständige Gruppe",
        related_name="responsible",
        blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        permissions = (("can_use", "Aufgabenverwaltung nutzen"), )

    base = models.ForeignKey(Ofahrt, verbose_name="Zugehörige OFahrt")

    name = models.CharField(
        "Aufgabe", max_length=255, help_text="Zusammenfassung der Aufgabe")
    description = models.TextField(
        "Beschreibung",
        blank=True,
        help_text="Ausführlichere Beschreibung der Aufgabe (optional)")
    category = models.ForeignKey(
        TaskCategory,
        verbose_name="Kategorie",
        help_text=
        "Über die Kategorie wird geregelt, welche Benutzer Zugriff auf dieses Ticket haben"
    )

    PRIORITY_CHOICES = (("optional", "optional"), ("unwichtig", "unwichtig"),
                        ("normal", "normal"), ("wichtig", "wichtig"),
                        ("dringend", "dringend"))

    priority = models.CharField(
        "Priorität",
        max_length=30,
        choices=PRIORITY_CHOICES,
        default="normal",
        help_text="Die Priorität gibt an wie dringend das Ticket ist.")

    STATUS_CHOICES = (("neu", "neu"), ("zugewiesen", "zugewiesen"),
                      ("erledigt", "erledigt"), ("abgebrochen", "abgebrochen"))

    status = models.CharField(
        "Status", max_length=30, choices=STATUS_CHOICES, default="neu")

    editors = models.ManyToManyField(
        User, verbose_name="Bearbeiter", blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Eingetragen am")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Verändert am")

    def __str__(self):
        return self.name


class TaskComment(models.Model):
    class Meta:
        verbose_name = "Kommentar"
        verbose_name_plural = "Kommentare"

    ticket = models.ForeignKey(Task, verbose_name="Zugehöriges Ticket")
    user = models.ForeignKey(User, verbose_name="Autor")
    text = models.TextField(
        "Kommentartext",
        help_text="Gib hier den Text an, den dein Kommentar enthalten soll.")
    timestamp = models.DateTimeField("Zeitpunkt")

    def __str__(self):
        return "(" + self.user.__str__() + ") " + self.ticket.__str__(
        ) + ": " + self.text[:50] + "..."


class TaskHistoryEntry(models.Model):
    class Meta:
        verbose_name = "Historyeintrag"
        verbose_name_plural = "Historyeinträge"

    ticket = models.ForeignKey(Task, verbose_name="Zugehöriges Ticket")
    user = models.ForeignKey(
        User, verbose_name="Zugehöriger User", null=True, blank=True)
    text = models.CharField("Text", max_length=255)
    timestamp = models.DateTimeField("Zeitpunkt")

    def __str__(self):
        return "(" + self.user.__str__() + ") " + self.ticket.__str__(
        ) + ": " + self.text
