# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('SalesPeople', '0006_auto_20170718_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesteam',
            name='Team Sales',
            field=models.ManyToManyField(null=True, to='SalesPeople.Sale'),
        ),
    ]