# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-23 12:59
from __future__ import unicode_literals

import SalesPeople.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Meeting', 'Meeting'), ('Phone call', 'Phone call'), ('Email', 'Email')], default='Meeting', max_length=20)),
                ('activity_type', models.CharField(choices=[('Making contact', 'Making contact'), ('Establishing sale potential', 'Establishing sale potential'), ('Trying to make a sale', 'Trying to make a sale')], default='Making contact', max_length=50)),
                ('title', models.CharField(blank=True, default='Speak to team leader', max_length=32, verbose_name='Task title')),
                ('description', models.CharField(max_length=512, null=True, verbose_name='Task description')),
                ('activity_start_date', models.DateTimeField(verbose_name='Task start date and time')),
                ('activity_completion_date', models.DateTimeField(null=True, verbose_name='Task completion date and time')),
                ('activity_end_date', models.DateTimeField(verbose_name='Task end date and time')),
                ('completed', models.BooleanField(default=False, verbose_name='Claimed completed')),
                ('verified_completed', models.BooleanField(default=False, verbose_name='Verified complete by team leader')),
                ('Date added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('contact_number', models.CharField(max_length=10)),
                ('address', models.CharField(max_length=100)),
                ('qualified', models.BooleanField(default=False, verbose_name='Qualified')),
                ('Date added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyRepresentative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('contact_number', models.CharField(max_length=10)),
                ('email', models.EmailField(default='john_doe@kva.co.za', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', 'Dollar'), ('GBP', 'Pound'), ('ZAR', 'Rand')], default='ZAR', max_length=10, verbose_name='Currency')),
                ('rate_of_exchange', models.FloatField(default=1, verbose_name='R.O.E')),
                ('date_last_updated', models.DateField(default=django.utils.timezone.now, verbose_name='Last updated')),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_title', models.CharField(default='Make a million dollars', max_length=64, verbose_name='Goal title')),
                ('goal_description', models.CharField(default='Self-explanatory', max_length=256, verbose_name='Goal description')),
                ('goal_due_date', models.DateField(default=django.utils.timezone.now, verbose_name='Goal due date')),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Date added')),
                ('goal_completed', models.BooleanField(default=False, verbose_name='Goal completed')),
                ('Goal activities', models.ManyToManyField(to='SalesPeople.Activity')),
                ('sales_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReportFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filter_title', models.CharField(default='My filter', max_length=25, verbose_name='Filter title')),
                ('filter_description', models.CharField(max_length=256, null=True)),
                ('sale_completed', models.BooleanField(default=False, verbose_name='Sale closed')),
                ('filter_by_salesperson', models.BooleanField(default=True)),
                ('primary_sales_only', models.BooleanField(default=False)),
                ('show_all_sales', models.BooleanField(default=False)),
                ('filter_sales_by_team', models.BooleanField(default=False)),
                ('start_date_lower_bound', models.DateField(null=True, verbose_name='Start date lower bound')),
                ('start_date_upper_bound', models.DateField(null=True, verbose_name='Start date upper bound')),
                ('due_date_lower_bound', models.DateField(null=True, verbose_name='Due date lower bound')),
                ('due_date_upper_bound', models.DateField(null=True, verbose_name='Due date upper bound')),
                ('end_date_lower_bound', models.DateField(null=True, verbose_name='Close date lower bound')),
                ('end_date_upper_bound', models.DateField(null=True, verbose_name='Close date upper bound')),
                ('quoted_value_lower_bound', models.FloatField(null=True, verbose_name='Quoted value lower bound')),
                ('quoted_value_upper_bound', models.FloatField(null=True, verbose_name='Quoted value upper bound')),
                ('order_value_lower_bound', models.FloatField(null=True, verbose_name='Order value lower bound')),
                ('order_value_upper_bound', models.FloatField(null=True, verbose_name='Order value upper bound')),
                ('probability', models.CharField(choices=[('Blue Bird', 'Blue bird'), ('Probable', 'Probable'), ('Forecast', 'Forecast')], max_length=20, null=True, verbose_name='Sale probability')),
                ('status', models.CharField(choices=[('Blue Bird', 'Blue bird'), ('Probable', 'Probable'), ('Forecast', 'Forecast')], max_length=20, null=True, verbose_name='Sale status')),
                ('account', models.ManyToManyField(to='SalesPeople.Company', verbose_name='Account')),
                ('filter_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_owner', to=settings.AUTH_USER_MODEL, verbose_name='Filter owner')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_of_exchange', models.FloatField(default=1, verbose_name='Rate of exchange (when sale added)')),
                ('order_value', models.FloatField(default=0.0, verbose_name='Order Value')),
                ('quoted_value', models.FloatField(default=0, verbose_name='Quoted Value')),
                ('margin', models.FloatField(default=10, null=True, verbose_name='Margin (%)')),
                ('due_date', models.DateField(verbose_name='Date sale is due')),
                ('date_sale_completed', models.DateField(blank=True, null=True, verbose_name='Date of sale completion')),
                ('probability', models.CharField(choices=[('Blue Bird', 'Blue bird'), ('Probable', 'Probable'), ('Forecast', 'Forecast')], default='Probable', max_length=12, verbose_name='Sale Probability')),
                ('status', models.CharField(choices=[('Abandoned', 'Abandoned'), ('Lost', 'Lost'), ('Budget', 'Budget'), ('Won', 'Won'), ('In progress', 'In progress')], default='In progress', max_length=12, verbose_name='Sale Status')),
                ('sale_completed', models.BooleanField(default=False, verbose_name='Sale completed')),
                ('verified_completed', models.BooleanField(default=False, verbose_name='Verified completed')),
                ('unique_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='Optional unique reminder')),
                ('sale_description', models.CharField(max_length=256, null=True, verbose_name='Description')),
                ('quote_number', models.CharField(default='MPT', max_length=10, verbose_name='Quote Number')),
                ('Date added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.Company')),
                ('company_rep', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.CompanyRepresentative')),
                ('consultant', models.ManyToManyField(blank=True, related_name='consultant', to='SalesPeople.CompanyRepresentative', verbose_name='Consultant')),
                ('consulting_company', models.ManyToManyField(blank=True, related_name='consultant_company', to='SalesPeople.Company', verbose_name='Consulting company')),
                ('currency', models.ForeignKey(null=True, on_delete=SalesPeople.models.Currency, to='SalesPeople.Currency')),
                ('meetings', models.ManyToManyField(blank=True, to='SalesPeople.Activity')),
                ('other_salespeople', models.ManyToManyField(blank=True, related_name='secondary_salespeople', to=settings.AUTH_USER_MODEL)),
                ('prime_salesperson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prime_salesperson', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_leader', models.BooleanField(default=False, verbose_name='Team Leader')),
                ('contact_number', models.CharField(max_length=10)),
                ('total_sales_amount', models.FloatField(default=0)),
                ('pending_sales_amount', models.FloatField(default=0)),
                ('total_sales_count', models.IntegerField(default=0)),
                ('pending_sales_count', models.IntegerField(default=0)),
                ('Date added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalesTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=30, null=True, verbose_name='Branch name')),
                ('Date added', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('team_leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_leader_user', to=settings.AUTH_USER_MODEL)),
                ('team_members', models.ManyToManyField(blank=True, related_name='team_member_set', to=settings.AUTH_USER_MODEL)),
                ('team_sales', models.ManyToManyField(blank=True, to='SalesPeople.Sale')),
            ],
        ),
        migrations.CreateModel(
            name='SaleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_type', models.CharField(default='UC BMS', max_length=25, verbose_name='Item Type')),
                ('sale_description', models.CharField(default="R and D's developed UC for monitoringsecure power solutions on site. We should try sell more of these thanks totheir enormous margin", max_length=256, null=True, verbose_name='Description')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='sale_types',
            field=models.ManyToManyField(to='SalesPeople.SaleType', verbose_name='Type of sale (e.g. BMS)'),
        ),
        migrations.AddField(
            model_name='reportfilter',
            name='sale_type',
            field=models.ManyToManyField(to='SalesPeople.SaleType', verbose_name='Sale Type'),
        ),
        migrations.AddField(
            model_name='reportfilter',
            name='salesperson',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reportfilter',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.SalesTeam'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_representative',
            field=models.ManyToManyField(to='SalesPeople.CompanyRepresentative'),
        ),
        migrations.AddField(
            model_name='company',
            name='sales_representative',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.Company'),
        ),
        migrations.AddField(
            model_name='activity',
            name='company_representative',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='SalesPeople.CompanyRepresentative'),
        ),
        migrations.AddField(
            model_name='activity',
            name='consultant',
            field=models.ManyToManyField(related_name='consulting_company', to='SalesPeople.CompanyRepresentative'),
        ),
        migrations.AddField(
            model_name='activity',
            name='consulting_company',
            field=models.ManyToManyField(related_name='consultant', to='SalesPeople.Company'),
        ),
        migrations.AddField(
            model_name='activity',
            name='sales_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
