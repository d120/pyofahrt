from django.db import models
from django.db.utils import OperationalError
from datetime import date

class Ofahrt(models.Model):
    class Meta:
        verbose_name = "Ofahrtobjekt"
        verbose_name_plural = "Ofahrtobjekte"

    begin_date = models.DateField("Anreisedatum")
    end_date = models.DateField("Abreisedatum")

    active = models.BooleanField("Aktiv?", default=True, unique=True)

    def __str__(self):
        return "Ofahrt im Wintersemester " + str(self.begin_date.year)

    def current():
        try:
            return Ofahrt.objects.get(active=True)
        except (Ofahrt.DoesNotExist, OperationalError):
            return None

class Location(models.Model):
    class Meta:
        verbose_name = "Gelände"
        verbose_name_plural = "Gelände"


    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Building(models.Model):
    class Meta:
        verbose_name = "Gebäude"
        verbose_name_plural = "Gebäude"


    location = models.ForeignKey(Location)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Room(models.Model):
    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"

    building = models.ForeignKey(Building)
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=30)

    capacity = models.IntegerField("Kapazität", help_text="Wie viele Teilnehmer passen in diesen Raum?", default=0)

    usecase_sleep = models.BooleanField("Schlafraum", default=False)
    usecase_workshop = models.BooleanField("Workshops", default=False)
    usecase_outside = models.BooleanField("Freifläche", default=False)
    usecase_store = models.BooleanField("Lagerraum", default=False)
    usecase_meal = models.BooleanField("Essensraum", default=False)

    def __str__(self):
        return self.name

class Setting(models.Model):
    class Meta:
        verbose_name = "Einstellung"
        verbose_name_plural = "Einstellungen"
    key = models.CharField('Schlüssel', max_length=50, unique=True)
    readable = models.CharField("Eigenschaft", max_length=50, unique=True)
    value = models.BooleanField('Aktiv?')

    def get_Setting(keyx):
        if Ofahrt.current() == None:
            return False

        dicts = {
            "orga_reg_open": "Orgaregistrierung geöffnet",
            "workshop_reg_open": "Workshopanmeldung geöffnet",
            "member_reg_open": "Teilnehmerregistrierung geöffnet",
        }

        # Löscht veraltete Einträge
        Setting.objects.exclude(key__in=dicts).delete()

        temp = Setting.objects.filter(key=keyx)
        if temp.count() == 0:
            newtemp = Setting(key=keyx, value=False, readable=dicts[keyx])
            newtemp.save()
            temp = False
        else:
            temp = temp[0].value
        return temp



    def __str__(self):
        return self.key
