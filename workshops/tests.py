import datetime

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from workshops.models import Workshop
from ofahrtbase.models import Ofahrt

# Create your tests here.


class WorkshopTests(TestCase):

    def setUp(self):
        ofahrt = Ofahrt.objects.create(
            begin_date=datetime.date.today(), end_date=datetime.date.today()
        )
        ofahrt.save()
        self.w1 = Workshop.objects.create(name="Testworkshop", base=ofahrt)
        self.w1.save()
        self.user = User.objects.create_superuser(
            username="admin", email="admin@admin.de", password="admin"
        )
        self.user.save()
        self.client = Client()
        self.client.force_login(self.user)

    def test_workshop_set_accepted_action(self):
        self.w1.refresh_from_db()
        self.assertFalse(self.w1.accepted)
        self.assertFalse(self.w1.proved)

        self.client.post(
            reverse("admin:workshops_workshop_changelist"),
            {"action": "set_accepted", "_selected_action": self.w1.id},
            follow=True,
        )

        self.w1.refresh_from_db()
        self.assertTrue(self.w1.accepted)
        self.assertTrue(self.w1.proved)

    def test_workshop_tex_output(self):
        self.w1.accepted = True
        self.w1.proved = True
        self.w1.save()
        response = self.client.get(reverse('workshops:infoexport'), )
        with open('workshops/testfiles/workshops-export.tex', 'r') as f:
            self.assertEqual(
                response.content.decode(encoding='UTF-8'), f.read())
