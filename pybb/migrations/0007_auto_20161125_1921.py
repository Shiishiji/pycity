# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import pybb.util


class Migration(migrations.Migration):

    dependencies = [
        ('pybb', '0006_forum_subscriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file',
            field=models.FileField(upload_to=pybb.util.FilePathGenerator(to='pybb_upload\\attachments'), verbose_name='File'),
        ),
    ]