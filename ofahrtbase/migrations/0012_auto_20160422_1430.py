# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-22 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ofahrtbase', '0011_auto_20160422_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='value',
            field=models.BooleanField(verbose_name='Aktiv?'),
        ),
    ]
