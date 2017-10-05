# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lucivari', '0005_auto_20170921_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateFile',
            fields=[
                ('filename', models.TextField(blank=True, db_column='filename')),
                ('description', models.TextField(blank=True, db_column='Description', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'templates',
                'managed': False,
            },
        ),
    ]