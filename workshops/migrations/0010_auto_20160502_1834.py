# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 16:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0009_auto_20160502_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workshop',
            options={'permissions': (('editeveryworkshop', 'Jeden Workshop bearbeiten'), ('proveworkshop', 'Einen Workshop als geprüft markieren'), ('acceptworkshop', 'Einen Workshop als akzeptiert markieren')), 'verbose_name': 'Workshop', 'verbose_name_plural': 'Workshops'},
        ),
    ]
