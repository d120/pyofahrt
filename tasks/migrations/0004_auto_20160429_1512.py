# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 13:12
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20160429_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 29, 13, 12, 34, 818810, tzinfo=utc), verbose_name='Eingetragen am'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 29, 13, 12, 39, 848471, tzinfo=utc), verbose_name='Verändert am'),
            preserve_default=False,
        ),
    ]
