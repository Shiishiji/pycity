# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_profile_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='banned',
            field=models.NullBooleanField(default=False),
        ),
    ]