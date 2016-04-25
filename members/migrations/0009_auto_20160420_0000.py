# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20160419_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('m', 'männlich'), ('w', 'weiblich'), ('n', 'keines der genannten')], default='n', help_text='Diese Angabe wird nur für die Zuteilung der Schlafräume minderjähriger Teilnehmer verwendet.', max_length=25, verbose_name='Geschlecht'),
        ),
    ]
