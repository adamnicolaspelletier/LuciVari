# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-19 15:50
from __future__ import unicode_literals

from django.db import migrations, models
import lucivari.models


class Migration(migrations.Migration):

    dependencies = [
        ('lucivari', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=lucivari.models.content_file_name),
        ),
    ]
