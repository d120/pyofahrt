# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-07 11:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import workshops.models


class Migration(migrations.Migration):

    replaces = [('workshops', '0001_initial'), ('workshops', '0002_auto_20160429_1234'), ('workshops', '0003_workshop_slot'), ('workshops', '0004_auto_20160429_1242'), ('workshops', '0005_auto_20160429_1310'), ('workshops', '0006_workshop_base'), ('workshops', '0007_auto_20160502_1210'), ('workshops', '0008_workshop_requirements'), ('workshops', '0009_auto_20160502_1811'), ('workshops', '0010_auto_20160502_1834'), ('workshops', '0011_auto_20160502_1838'), ('workshops', '0012_auto_20160502_1851'), ('workshops', '0013_workshop_conditions'), ('workshops', '0014_auto_20160507_2153'), ('workshops', '0015_auto_20160825_1350'), ('workshops', '0016_auto_20161009_2033'), ('workshops', '0017_auto_20161009_2046'), ('workshops', '0018_auto_20161015_0024'), ('workshops', '0019_auto_20161015_1421'), ('workshops', '0020_auto_20161020_1719'), ('workshops', '0021_auto_20161020_1750'), ('workshops', '0022_slot_room'), ('workshops', '0023_auto_20161025_1652'), ('workshops', '0024_auto_20161101_2326'), ('workshops', '0025_auto_20161105_1451'), ('workshops', '0026_auto_20161109_1821'), ('workshops', '0027_auto_20161110_0311'), ('workshops', '0028_auto_20161110_1931'), ('workshops', '0029_auto_20170602_2056'), ('workshops', '0030_auto_20171012_1747'), ('workshops', '0031_auto_20171017_1201'), ('workshops', '0032_auto_20171025_1819')]

    initial = True

    dependencies = [
        ('ofahrtbase', '0013_remove_ofahrt_year'),
        ('ofahrtbase', '0019_auto_20161020_1750'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Titel')),
                ('description', models.TextField(blank=True, verbose_name='Beschreibung')),
                ('host', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Workshopanbieter')),
            ],
            options={
                'verbose_name': 'Workshop',
                'verbose_name_plural': 'Workshops',
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Bezeichnung')),
                ('begin', models.DateTimeField(default=workshops.models.Slot.defaultdate, verbose_name='Start')),
                ('end', models.DateTimeField(default=workshops.models.Slot.defaultdate, verbose_name='Ende')),
                ('priority', models.CharField(choices=[('opt', 'optional'), ('zentral', 'zentral'), ('dezentral', 'dezentral'), ('wichtig', 'wichtig')], default='zentral', max_length=30, verbose_name='Priorität')),
                ('slottype', models.CharField(choices=[('workshop', 'Workshop'), ('event', 'Zentrale Veranstaltung'), ('food', 'Essen'), ('sonstiges', 'Sonstiges')], default='sonstiges', max_length=30, verbose_name='Art des Slots')),
            ],
            options={
                'verbose_name': 'Zeitslot',
                'verbose_name_plural': 'Zeitslots',
            },
        ),
        migrations.AddField(
            model_name='workshop',
            name='slot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='workshops.Slot', verbose_name='Zugeteilter Zeitslot'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='base',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofahrtbase.Ofahrt', verbose_name='Zugehörige Ofahrt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workshop',
            name='accepted',
            field=models.BooleanField(default=False, help_text='Workshopidee ist in Ordnung', verbose_name='Akzeptiert'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='proved',
            field=models.BooleanField(default=False, help_text='Der aktuelle Workshopstand ist durch den Workshoporga geprüft.', verbose_name='Geprüft'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='requirements',
            field=models.TextField(blank=True, verbose_name='Materialbedarf'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='host',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Workshopanbieter'),
        ),
        migrations.AlterModelOptions(
            name='workshop',
            options={'permissions': (('can_use', 'Die Workshopkomponente nutzen'), ('editeveryworkshop', 'Jeden Workshop bearbeiten'), ('proveworkshop', 'Einen Workshop als geprüft markieren'), ('acceptworkshop', 'Einen Workshop als akzeptiert markieren'), ('assignworkshop', 'Workshopzuweisung ändern')), 'verbose_name': 'Workshop', 'verbose_name_plural': 'Workshops'},
        ),
        migrations.AddField(
            model_name='workshop',
            name='conditions',
            field=models.TextField(blank=True, verbose_name='Teilnahmebedingungen'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='maxmembers',
            field=models.IntegerField(blank=True, default=0, verbose_name='Maximale Teilnehmerzahl'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='otherstuff',
            field=models.TextField(blank=True, verbose_name='Sonstiges'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ofahrtbase.Room', verbose_name='Zugeteilter Raum'),
        ),
        migrations.AlterModelOptions(
            name='workshop',
            options={'permissions': (('can_use', 'Die Workshopkomponente nutzen'), ('editeveryworkshop', 'Jeden Workshop bearbeiten'), ('proveworkshop', 'Einen Workshop als geprüft markieren'), ('acceptworkshop', 'Einen Workshop als akzeptiert markieren'), ('assignworkshop', 'Workshopzuweisung ändern'), ('viewemails', 'E-Mails der Workshopanbieter*innen einsehen')), 'verbose_name': 'Workshop', 'verbose_name_plural': 'Workshops'},
        ),
    ]
