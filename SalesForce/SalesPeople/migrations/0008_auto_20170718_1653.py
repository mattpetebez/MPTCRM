# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 14:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('SalesPeople', '0007_auto_20170718_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='other_salespeople',
            field=models.ManyToManyField(null=True, related_name='secondary_salespeople', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='salesteam',
            name='Team Sales',
            field=models.ManyToManyField(blank=True, null=True, to='SalesPeople.Sale'),
        ),
    ]