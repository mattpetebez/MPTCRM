# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 13:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SalesPeople', '0005_auto_20170502_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesperson',
            name='email_address',
            field=models.CharField(default='babababa', max_length=30),
        ),
    ]
