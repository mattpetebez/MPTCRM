# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 05:59
from __future__ import unicode_literals

from django.db import migrations, models

import SalesPeople.models


class Migration(migrations.Migration):
    dependencies = [
        ('SalesPeople', '0010_auto_20170630_0814'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='potential', max_length=10, verbose_name='Sale Status')),
            ],
        ),
        migrations.AlterField(
            model_name='sale',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=SalesPeople.models.Company,
                                    to='SalesPeople.Company'),
        ),
    ]
