# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-04 16:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_banned'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='banned',
        ),
    ]
