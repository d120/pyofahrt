# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-12 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import workshops.models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0029_auto_20170602_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='begin',
            field=models.DateTimeField(default=workshops.models.Slot.defaultdate, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='end',
            field=models.DateTimeField(default=workshops.models.Slot.defaultdate, verbose_name='Ende'),
        ),
    ]