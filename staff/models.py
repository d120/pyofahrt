from django.db import models
from ofahrtbase.models import Ofahrt, Room
from django.db.models.query_utils import Q
from django.contrib.auth.models import Group, Permission, User

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


class StaffBarcode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kdv_barcode = models.IntegerField("KDV-Barcode", null=True, blank=True, unique=True)

class StaffRoomAssignement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, verbose_name = "Zugeteilter Raum", null=True, blank=True)

class StaffTagBox(models.Model):
    class Meta:
        verbose_name = "Tagbox"
        verbose_name_plural = "Tagboxen"

    group = models.OneToOneField(Group, on_delete=models.CASCADE)

    letter = models.CharField("Key", unique=True, max_length=3)
    text = models.CharField("Text", unique=True, max_length=10)

    def __str__(self):
        return ""


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

    workshop_ideas = models.TextField("Workshopidee(n)", help_text='Bei mehreren Ideen, bitte eine Zeile pro Idee verwenden. Die Ideen sollen nur grob umrissen werden. Ein ausführlicherer Text wird erst an späterer Stelle benötigt.')


def get_nametag_boxes(self):
    out = []

    for group in self.groups.all():
        try:
            box = StaffTagBox.objects.get(group=group)
            out.append("\\Tagbox{ " + box.letter + " }{ " + box.text + " }")
        except StaffTagBox.DoesNotExist:
            out.append("\\Tagbox{ " + group.name[0] + " }{ " + group.name + " }")

    while len(out) < 4:
        out.append("~")

    if self.is_staff:
        #Person ist Orga
        out.append("\\Tagbox{ O }{ ORGA }")
    else:
        #Person ist "nur" Workshopanbieter
        out.append("\\Tagbox{ WS }{ WORKSHOP }")

    return list(reversed(out))

def get_kdv_barcode(self):
    return StaffBarcode.objects.get(user=self).kdv_barcode


def get_room(self):
    try:
        temp = StaffRoomAssignement.objects.get(user=self).room
    except StaffRoomAssignement.DoesNotExist:
        temp = StaffRoomAssignement(user=self)
        temp.save()
    return temp


User.add_to_class('get_nametag_boxes', get_nametag_boxes)
User.add_to_class('get_kdv_barcode', get_kdv_barcode)
User.add_to_class('get_room', get_room)
