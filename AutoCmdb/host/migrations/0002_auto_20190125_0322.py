# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-01-24 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='os_version',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='系統版本'),
        ),
    ]
