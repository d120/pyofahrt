# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-07 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('faq', '0001_initial'), ('faq', '0002_auto_20160420_1233'), ('faq', '0003_auto_20160422_1347')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaqCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Frage')),
                ('answer', models.TextField(verbose_name='Antwort')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faq.FaqCategory', verbose_name='Kategorie')),
            ],
            options={
                'verbose_name': 'Frage',
                'verbose_name_plural': 'Fragen',
            },
        ),
        migrations.AlterModelOptions(
            name='faqcategory',
            options={'verbose_name': 'Kategorie', 'verbose_name_plural': 'Kategorien'},
        ),
    ]
