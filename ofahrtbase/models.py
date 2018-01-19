from django.db import models
from django.db.utils import OperationalError
from datetime import date


class Ofahrt(models.Model):
    class Meta:
        verbose_name = "Ofahrtobjekt"
        verbose_name_plural = "Ofahrtobjekte"

    begin_date = models.DateField("Anreisedatum")
    end_date = models.DateField("Abreisedatum")

    # Einstellungen
    ## Booleans
    orga_reg_open = models.BooleanField(
        "Orgaregistrierung",
        help_text=
        "Ist dieser Wert aktiviert, können sich Studierende als Ofahrtorga bewerben.",
        default=False)
    workshop_reg_open = models.BooleanField(
        "Workshopregistrierung",
        help_text=
        "Ist dieser Wert aktiviert, werden derzeit Workshops gesucht.",
        default=False)
    member_reg_open = models.BooleanField(
        "Teilnehmeregistrierung",
        help_text=
        "Ist dieser Wert aktiviert, können sich Teilnehmer*innen registrieren.",
        default=False)

    ## Integers
    max_members = models.IntegerField(
        "Maximale Teilnehmendenzahl",
        help_text=
        "Dieser Wert bestimmt die maximale Größe der Festanmeldeliste.",
        default=70)
    queue_tolerance = models.IntegerField(
        "Warteschlangentoleranz",
        help_text=
        "Dieser Wert legt fest, ab wann Neuanmeldungen von Teilnehmer*innen in die Warteschlange müssen. (Warteschlange falls: aktuelle Festanmeldungen + aktuell vorläufige Anmeldungen > maximale Festanmeldungen + dieser Wert)",
        default=20)
    self_participation = models.IntegerField(
        "Teilnahmebeitrag",
        help_text="Eingenanteil der Teilnehmer*innen in Cent",
        default=2000)

    active = models.BooleanField("Aktiv?", default=False)

    def save(self, *args, **kwargs):
        if self.active:
            Ofahrt.objects.all().update(**{'active': False})
        super(Ofahrt, self).save(*args, **kwargs)

    def __str__(self):
        return "Ofahrt im Wintersemester " + str(self.begin_date.year)

    @staticmethod
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

    capacity = models.IntegerField(
        "Kapazität",
        help_text="Wieviele Teilnehmer*innen passen in diesen Raum?",
        default=0)

    usecase_sleep = models.BooleanField("Schlafzimmer", default=False)
    usecase_workshop = models.BooleanField("Aktivitätenraum", default=False)
    usecase_outside = models.BooleanField("Freifläche", default=False)
    usecase_store = models.BooleanField("Lagerraum", default=False)
    usecase_meal = models.BooleanField("Speisesaal", default=False)

    def get_staff_users(self):
        out = []
        for user in self.staffroomassignment_set.all():
            out.append(user.user)
        return out

    def get_staff_users_count(self):
        return len(self.get_staff_users())

    def get_person_count(self):
        return self.get_member_users_count() + self.get_staff_users_count()

    def get_member_users(self):
        return self.member_set.all()

    def get_member_users_count(self):
        return len(self.get_member_users())

    def __str__(self):
        if self.number == "-1":
            return self.name
        else:
            return self.name + " (Nr. " + self.number + ")"
