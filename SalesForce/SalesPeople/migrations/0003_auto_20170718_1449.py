# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 12:49
from __future__ import unicode_literals

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):
    dependencies = [
        ('SalesPeople', '0002_auto_20170718_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 18, 12, 49, 10, 488667, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='company',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 18, 12, 49, 10, 486174, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='goal',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 18, 12, 49, 10, 496085, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='salesperson',
            name='Date added',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 18, 12, 49, 10, 483756, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='salesteam',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 18, 12, 49, 10, 494057, tzinfo=utc)),
        ),
    ]
