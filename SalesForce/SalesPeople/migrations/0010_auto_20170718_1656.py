# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-18 14:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('SalesPeople', '0009_auto_20170718_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='consultant',
            field=models.ManyToManyField(blank=True, null=True, related_name='consultant',
                                         to='SalesPeople.CompanyRepresentative'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='consulting_company',
            field=models.ManyToManyField(blank=True, null=True, related_name='consultant_company',
                                         to='SalesPeople.Company'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='other_salespeople',
            field=models.ManyToManyField(blank=True, related_name='secondary_salespeople', to=settings.AUTH_USER_MODEL),
        ),
    ]
