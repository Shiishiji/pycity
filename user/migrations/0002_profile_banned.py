# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='banned',
            field=models.BooleanField(default=False),
        ),
    ]
