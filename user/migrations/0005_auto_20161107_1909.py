# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 18:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profile_banned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='banned',
            field=models.BooleanField(default=False),
        ),
    ]