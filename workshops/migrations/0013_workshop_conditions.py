# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-06 12:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0012_auto_20160502_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='conditions',
            field=models.TextField(blank=True, verbose_name='Teilnahmebedingunden'),
        ),
    ]
