# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.


class SalesPerson(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    team_leader = models.BooleanField('Team Leader', default=False)
    contact_number = models.CharField(max_length=10)
    total_sales_amount = models.FloatField(default=0)
    pending_sales_amount = models.FloatField(default=0)
    total_sales_count = models.IntegerField(default=0)
    pending_sales_count = models.IntegerField(default=0)
    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return str(self.user.first_name)

    def clear_counters(self):
        self.total_sales_amount = 0
        self.total_sales_count = 0
        self.pending_sales_amount = 0
        self.pending_sales_count = 0
        self.save()


class CompanyRepresentative(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Company(models.Model):
    company_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    company_representative = models.ManyToManyField(CompanyRepresentative, name='Company Representatives')
    sales_representative = models.ManyToManyField(User)
    address = models.CharField(max_length=20)
    qualified = models.BooleanField('Qualified', default=False)
    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return self.company_name


class Activity(models.Model):
    meeting = "Meeting"
    phone_call = "Phone call"
    email = "Email"

    activity_choices = (
        (meeting, "Meeting"),
        (phone_call, "Phone call"),
        (email, "Email"),
    )

    attempting_connection = "Making contact"
    attempting_qualification = "Establishing sale potential"
    attempting_sale = "Trying to make a sale"

    activity_type_choices = (
        (attempting_connection, "Making contact"),
        (attempting_qualification, "Establishing sale potential"),
        (attempting_sale, "Trying to make a sale"),
    )

    sales_person = models.ForeignKey(User, null=True, blank=True)

    activity = models.CharField(max_length=20, choices=activity_choices, default=meeting)
    activity_type = models.CharField(max_length=50, choices=activity_type_choices, default=attempting_connection)

    company_representative = models.ForeignKey(CompanyRepresentative, null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    title = models.CharField('Task title', max_length=32, default="Speak to team leader for more details", blank=True)
    description = models.CharField('Task description', max_length=512, null=True)

    activity_start_date = models.DateTimeField('Task start date and time')
    activity_completion_date = models.DateTimeField('Task completion date and time')
    activity_end_date = models.DateTimeField('Task end date and time')

    completed = models.BooleanField('Submitted completed', default=False)
    verified_completed = models.BooleanField('Verified complete by team leader', default=False)

    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return_val = "%s: %s (%s)" % (self.company.company_name, self.title, self.activity_type)
        return return_val


# A model for defining whether its a datacentre, BMS or something like that
class SaleType(models.Model):
    models.CharField('Sale Type', max_length=20, null=True)


class Sale(models.Model):
    blue_bird = "Blue Bird"
    probable = "Probable"
    forecast = "Forecast"

    probability_choices = (
        (blue_bird, "Blue bird"),
        (probable, "Probable"),
        (forecast, "Forecast"),
    )

    abandoned = "Abandoned"
    lost = "Lost"
    budget = "Budget"
    won = "Won"
    in_progress = "In progress"
    # Need a class for goals set by the administrator of the team.

    status_choices = (
        (abandoned, "Abandoned"),
        (lost, 'Lost'),
        (budget, 'Budget'),
        (won, 'Won'),
        (in_progress, 'In progress'),
    )

    value = models.FloatField('Value in Rands', default=0.00)

    due_date = models.DateField('Date sale is due')
    date_sale_completed = models.DateField('Date of sale completion', null=True, blank=True)

    probability = models.CharField('Sale Probability', max_length=12, choices=probability_choices, default=probable)
    status = models.CharField('Sale Status', max_length=12, choices=status_choices, default=in_progress)
    sale_completed = models.BooleanField('Sale closed', default=False)

    meetings = models.ManyToManyField(Activity, blank=True)

    prime_salesperson = models.ForeignKey(User, related_name='prime_salesperson', null=True)
    other_salespeople = models.ManyToManyField(User, related_name='secondary_salespeople', blank=True)

    company_rep = models.ForeignKey(CompanyRepresentative, blank=True, null=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    consulting_company = models.ManyToManyField(Company, related_name="consultant_company", blank=True)
    consultant = models.ManyToManyField(CompanyRepresentative, related_name="consultant", blank=True)

    unique_id = models.CharField('Optional unique reminder', blank=True, null=True, max_length=20)
    sale_description = models.CharField('Description', null=True, max_length=256)

    quote_number = models.CharField('Quote Number', default="MPT", max_length=10)

    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        company_name = (Company.objects.get(id=self.company_id)).company_name
        if not self.unique_id:
            return "%s: R%0.2f" % (company_name, self.value)
        else:
            return "%s: %s" % (company_name, self.unique_id)

    def sync_sale_add(self):
        for user in self.other_salespeople.all():
            if self.sale_completed:
                user.salesperson.total_sales_amount += self.value
                user.salesperson.pending_sales_amount -= self.value
                user.salesperson.total_sales_count += 1
                user.salesperson.pending_sales_count -= 1
                user.salesperson.save()
            else:
                user.salesperson.pending_sales_amount += self.value
                user.salesperson.pending_sales_count += 1
                user.salesperson.save()

    def assign_quote_number(self):
        self.quote_number = ("MPT%d" % self.id)

    def get_age(self):
        return timezone.now() - self.date_added


class SalesTeam(models.Model):
    team_leader = models.ForeignKey(User, null=True, related_name="team_leader_user")
    team_members = models.ManyToManyField(User, blank=True, related_name="team_member_set")
    branch_name = models.CharField('Branch name', null=True, max_length=30)
    team_sales = models.ManyToManyField(Sale, blank=True)

    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return "%s team" % self.branch_name


# Need a class for goals set by the administrator of the team.


class Goal(models.Model):
    sales_person = models.ForeignKey(User, name='Sales Person Goal set', null=True)
    activities = models.ManyToManyField(Activity, name='Goal activities')
    goal_title = models.CharField(max_length=64, name="Goal title", default="Make a million dollars")
    goal_description = models.CharField(max_length=256, name='Goal description', default="Self-explanatory")

    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return self.goal_title
