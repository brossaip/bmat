# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 09:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0003_topplay'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topplay',
            name='plays',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='topplay',
            name='previous_plays',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='topplay',
            name='previous_rank',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
