# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-09 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0015_auto_20160825_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='maxmembers',
            field=models.IntegerField(blank=True, default=0, verbose_name='Maximale Teilnehmer'),
        ),
        migrations.AddField(
            model_name='workshop',
            name='otherstuff',
            field=models.TextField(blank=True, verbose_name='Maximale Teilnehmer'),
        ),
    ]