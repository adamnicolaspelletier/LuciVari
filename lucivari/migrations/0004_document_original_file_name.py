# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 15:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lucivari', '0003_auto_20170919_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='original_file_name',
            field=models.CharField(default=django.utils.timezone.now, editable=False, max_length=255),
            preserve_default=False,
        ),
    ]
