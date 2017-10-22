# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0018_auto_20171016_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgacandidate',
            name='roommate_preference',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Gewünschte Zimmernachbarn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='workshopcandidate',
            name='roommate_preference',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Gewünschte Zimmernachbarn'),
            preserve_default=False,
        ),
    ]
