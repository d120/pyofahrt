# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofahrtbase', '0019_auto_20161020_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ofahrt',
            name='max_members',
            field=models.IntegerField(default=70, help_text='Dieser Wert bestimmt die maximale Größe der Festanmeldeliste.', verbose_name='Maximale Teilnehmendenzahl'),
        ),
        migrations.AlterField(
            model_name='ofahrt',
            name='member_reg_open',
            field=models.BooleanField(default=False, help_text='Ist dieser Wert aktiviert, können sich Teilnehmer*innen registrieren.', verbose_name='Teilnehmeregistrierung'),
        ),
        migrations.AlterField(
            model_name='ofahrt',
            name='orga_reg_open',
            field=models.BooleanField(default=False, help_text='Ist dieser Wert aktiviert, können sich Studierende als Ofahrtorga bewerben.', verbose_name='Orgaregistrierung'),
        ),
        migrations.AlterField(
            model_name='ofahrt',
            name='queue_tolerance',
            field=models.IntegerField(default=20, help_text='Dieser Wert legt fest, ab wann Neuanmeldungen von Teilnehmer*innen in die Warteschlange müssen. (Warteschlange falls: aktuelle Festanmeldungen + aktuell vorläufige Anmeldungen > maximale Festanmeldungen + dieser Wert)', verbose_name='Warteschlangentoleranz'),
        ),
        migrations.AlterField(
            model_name='ofahrt',
            name='self_participation',
            field=models.IntegerField(default=2000, help_text='Eingenanteil der Teilnehmer*innen in Cent', verbose_name='Teilnahmebeitrag'),
        ),
        migrations.AlterField(
            model_name='ofahrt',
            name='workshop_reg_open',
            field=models.BooleanField(default=False, help_text='Ist dieser Wert aktiviert, werden derzeit Workshops gesucht.', verbose_name='Workshopregistrierung'),
        ),
    ]