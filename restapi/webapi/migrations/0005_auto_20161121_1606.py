# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapi', '0004_auto_20161118_0922'),
    ]

    operations = [
        migrations.CreateModel(
            name='TopPlayPrevious',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_plays', models.IntegerField()),
                ('previous_rank', models.IntegerField(blank=True, null=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapi.Song')),
            ],
        ),
        migrations.RemoveField(
            model_name='topplay',
            name='song',
        ),
        migrations.DeleteModel(
            name='TopPlay',
        ),
    ]
