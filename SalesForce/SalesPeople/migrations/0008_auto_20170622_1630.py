# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 14:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SalesPeople', '0007_auto_20170502_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='sales_representative',
        ),
        migrations.AddField(
            model_name='company',
            name='sales_representative',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]