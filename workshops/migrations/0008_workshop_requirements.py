# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0007_auto_20160502_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='requirements',
            field=models.TextField(blank=True, verbose_name='Materialbedarf'),
        ),
    ]