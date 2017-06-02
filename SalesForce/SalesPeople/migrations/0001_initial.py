# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-28 15:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyRepresentative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('contact_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting_date', models.DateTimeField(verbose_name='Date and time of meeting')),
                ('proactive', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.Company')),
                ('company_representative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.CompanyRepresentative')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0)),
                ('date_acquired', models.DateField(verbose_name='Date sale was acquired')),
                ('due_date', models.DateField(verbose_name='Date sale is due')),
                ('sale_completed', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.Company')),
                ('company_rep', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.CompanyRepresentative')),
                ('meetings', models.ManyToManyField(blank=True, to='SalesPeople.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('contact_number', models.CharField(max_length=10)),
                ('email_address', models.CharField(max_length=40, null=True)),
                ('total_sales_amount', models.FloatField(default=0)),
                ('pending_sales_amount', models.FloatField(default=0)),
                ('total_sales_count', models.IntegerField(default=0)),
                ('pending_sales_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='sales_people',
            field=models.ManyToManyField(blank=True, to='SalesPeople.SalesPerson'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.SalesPerson'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.CompanyRepresentative'),
        ),
        migrations.AddField(
            model_name='company',
            name='sales_representative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.SalesPerson'),
        ),
    ]
