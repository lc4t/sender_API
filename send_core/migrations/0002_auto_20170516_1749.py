# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-16 17:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('send_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='update_time',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 16, 17, 49, 54, 628079)),
        ),
    ]
