# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-10-17 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0030_auto_20171012_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workshop',
            name='maxmembers',
            field=models.IntegerField(blank=True, default=0, verbose_name='Maximale Teilnehmerzahl'),
        ),
    ]