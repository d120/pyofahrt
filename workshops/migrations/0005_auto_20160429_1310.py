# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0004_auto_20160429_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='priority',
            field=models.CharField(
                choices=[('opt', 'optional'), ('zentral', 'zentral'),
                         ('dezentral', 'dezentral'), ('wichtig', 'wichtig')],
                default='zentral',
                max_length=30,
                verbose_name='Priorität'),
        ),
        migrations.AddField(
            model_name='slot',
            name='slottype',
            field=models.CharField(
                choices=[('workshop', 'Workshop'), ('event',
                                                    'Zentrale Veranstaltung'),
                         ('food', 'Essen'), ('sonstiges', 'Sonstiges')],
                default='sonstiges',
                max_length=30,
                verbose_name='Art des Slots'),
        ),
        migrations.AlterField(
            model_name='slot',
            name='name',
            field=models.CharField(
                max_length=30, unique=True, verbose_name='Bezeichnung'),
        ),
    ]
