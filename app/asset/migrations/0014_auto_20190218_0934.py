# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-18 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_auto_20190218_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assettoassets',
            old_name='name',
            new_name='asset_obj',
        ),
        migrations.RemoveField(
            model_name='assettoassets',
            name='asset_objs',
        ),
        migrations.AddField(
            model_name='assettoassets',
            name='assets',
            field=models.ManyToManyField(related_name='_assettoassets_assets_+', to='asset.Asset', verbose_name='關聯資產'),
        ),
    ]
