# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ofahrtbase', '0012_auto_20160422_1430'),
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name='Vorname')),
                ('last_name', models.CharField(max_length=30, verbose_name='Nachname')),
                ('email', models.EmailField(max_length=254, verbose_name='Email-Adresse')),
                ('phone', models.CharField(max_length=30, verbose_name='Handynummer')),
                ('want_to_be_orga', models.BooleanField(verbose_name='Orga')),
                ('want_to_be_wl', models.BooleanField(verbose_name='Workshopanbieter')),
                ('workshop_ideas', models.TextField(help_text='Mehrere Ideen bitte in verschiedenen Zeilen unterbringen', verbose_name='Ideen für Workshops')),
                ('base', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofahrtbase.Ofahrt', verbose_name='Zugehörige Ofahrt')),
                ('orga_for', models.ManyToManyField(related_name='Orgajob', to='auth.Group')),
            ],
        ),
    ]
