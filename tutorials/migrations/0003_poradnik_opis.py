# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-25 00:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0002_kategoria_opis'),
    ]

    operations = [
        migrations.AddField(
            model_name='poradnik',
            name='opis',
            field=models.CharField(default='', max_length=150),
        ),
    ]
