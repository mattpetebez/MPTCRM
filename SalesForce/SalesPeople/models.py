# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import django


# Create your models here.

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


def get_user_first_name(self):
    return self.first_name + ' ' + self.last_name

User.add_to_class('__str__', get_user_first_name)


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
    email = models.EmailField(max_length=100, default='john_doe@kva.co.za')

    def __str__(self):
        if self.company_set.get():
            return "%s %s: %s" % (self.first_name, self.last_name, self.company_set.get().company_name)
        else:
            return "%s %s" % (self.first_name, self.last_name)


class Company(models.Model):
    company_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    company_representative = models.ManyToManyField(CompanyRepresentative)
    sales_representative = models.ManyToManyField(User)
    address = models.CharField(max_length=100)
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

    sales_person = models.ForeignKey(User, null=True)

    action = models.CharField(max_length=20, choices=activity_choices, default=meeting)
    activity_type = models.CharField(max_length=50, choices=activity_type_choices, default=attempting_connection)

    company_representative = models.ForeignKey(CompanyRepresentative, null=True)
    company = models.ForeignKey(Company)

    consultant = models.ManyToManyField(CompanyRepresentative, related_name='consulting_company')
    consulting_company = models.ManyToManyField(Company, related_name='consultant')

    title = models.CharField('Task title', max_length=32, default="Speak to team leader", blank=True)
    description = models.CharField('Task description', max_length=512, null=True)

    activity_start_date = models.DateTimeField('Task start date and time')
    activity_completion_date = models.DateTimeField('Task completion date and time', null=True)
    activity_end_date = models.DateTimeField('Task end date and time')

    completed = models.BooleanField('Claimed completed', default=False)
    verified_completed = models.BooleanField('Verified complete by team leader', default=False)

    date_added = models.DateTimeField(name="Date added", default=timezone.now, editable=False)

    def __str__(self):
        return_val = "%s: %s (%s)" % (self.company.company_name, self.title, self.activity_type)
        return return_val


class Currency(models.Model):
    US_Dollar = "USD"
    GBP = "GBP"
    Rand = "ZAR"

    currency_choices = (
        (US_Dollar, "Dollar"),
        (GBP, 'Pound'),
        (Rand, 'Rand')
    )
    currency = models.CharField('Currency', max_length=10, choices=currency_choices, default=Rand)
    rate_of_exchange = models.FloatField('R.O.E', default=1)
    date_last_updated = models.DateField(verbose_name="Last updated", default=timezone.now)

    def __str__(self):
        return self.currency


# A model for defining whether its a data centre, BMS or something like that
class SaleType(models.Model):
    sale_type = models.CharField('Item Type', max_length=25, default='UC BMS')
    sale_description = models.CharField('Description', max_length=256, default="R and D's developed UC for monitoring"
                                                                               "secure power solutions on site. We "
                                                                               "should try sell more of these thanks to"
                                                                               "their enormous margin", null=True)

    def __str__(self):
        return self.sale_type


class Sale(models.Model):

    sale_types = models.ManyToManyField(SaleType, verbose_name="Type of sale (e.g. BMS)")
    currency = models.ForeignKey('Currency', Currency, null=True)
    rate_of_exchange = models.FloatField(verbose_name='Rate of exchange (when sale added)', default=1)
    order_value = models.FloatField('Order Value', default=0.00)
    quoted_value = models.FloatField('Quoted Value', default=0)
    margin = models.FloatField(verbose_name='Margin (%)', default=10, null=True)

    due_date = models.DateField('Date sale is due')
    date_sale_completed = models.DateField('Date of sale completion', null=True, blank=True)

    probability = models.CharField('Sale Probability', max_length=12, choices=probability_choices, default=probable)
    status = models.CharField('Sale Status', max_length=12, choices=status_choices, default=in_progress)
    sale_completed = models.BooleanField('Sale completed', default=False)
    verified_completed = models.BooleanField('Verified completed', default=False)

    activities = models.ManyToManyField(Activity, blank=True, name='meetings')

    prime_salesperson = models.ForeignKey(User, related_name='prime_salesperson', null=True)
    other_salespeople = models.ManyToManyField(User, related_name='secondary_salespeople', blank=True)

    company_rep = models.ForeignKey(CompanyRepresentative)
    company = models.ForeignKey(Company, null=True, blank=True)

    consulting_company = models.ManyToManyField(Company, verbose_name='Consulting company',
                                                related_name="consultant_company", blank=True)
    consultant = models.ManyToManyField(CompanyRepresentative, verbose_name='Consultant', related_name="consultant",
                                        blank=True)

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

    date_added = models.DateTimeField(name="Date added", default=django.utils.timezone.now, editable=False)

    def __str__(self):
        return "%s team" % self.branch_name


# Need a class for goals set by the administrator of the team.


class Goal(models.Model):
    sales_person = models.ForeignKey(User, null=True)
    goal_activities = models.ManyToManyField(Activity, name='Goal activities')
    goal_title = models.CharField('Goal title', max_length=64, default="Make a million dollars")
    goal_description = models.CharField('Goal description', max_length=256, default="Self-explanatory")
    goal_due_date = models.DateField('Goal due date', default=django.utils.timezone.now)
    date_added = models.DateTimeField("Date added", default=timezone.now, editable=False)
    goal_completed = models.BooleanField('Goal completed', default=False)

    def __str__(self):
        return self.goal_title


class ReportFilter(models.Model):

    # Title for the filter:
    filter_title = models.CharField(verbose_name='Filter title', max_length=25, default="My filter")
    filter_description = models.CharField(max_length=256, null=True)

    # Filter owner:
    filter_owner = models.ForeignKey(User, verbose_name="Filter owner", related_name="filter_owner", null=True)
    # Filter by Sale Completed
    sale_completed = models.BooleanField(default=False, verbose_name='Sale closed')
    # Filter by SalesPerson who as these sales as primary sales
    filter_by_salesperson = models.BooleanField(default=True)  # only if admin or team leader
    salesperson = models.ManyToManyField(User)  # only if admin or team leader
    primary_sales_only = models.BooleanField(default=False)

    # Sales person dealt with
    show_all_sales = models.BooleanField(default=False)  # only if admin
    filter_sales_by_team = models.BooleanField(default=False)  # only team leader or admin
    team = models.ForeignKey(SalesTeam, null=True)

    # Filter by account (company)
    account = models.ManyToManyField(Company, verbose_name="Account")

    # Filter by Sale Type
    sale_type = models.ManyToManyField(SaleType, verbose_name="Sale Type")

    # Filter by dates
    start_date_lower_bound = models.DateField('Start date lower bound', null=True)
    start_date_upper_bound = models.DateField('Start date upper bound', null=True)
    due_date_lower_bound =  models.DateField('Due date lower bound', null=True)
    due_date_upper_bound = models.DateField('Due date upper bound', null=True)
    end_date_lower_bound = models.DateField('Close date lower bound', null=True)
    end_date_upper_bound = models.DateField('Close date upper bound', null=True)

    # Filter by sale values
    quoted_value_lower_bound = models.FloatField('Quoted value lower bound', null=True)
    quoted_value_upper_bound = models.FloatField('Quoted value upper bound', null=True)
    order_value_lower_bound = models.FloatField('Order value lower bound', null=True)
    order_value_upper_bound = models.FloatField('Order value upper bound', null=True)

    # Filter by probability
    probability = models.CharField(verbose_name='Sale probability', choices=probability_choices, null=True,
                                   max_length=20)

    # Filter by sale status
    status = models.CharField(verbose_name='Sale status', choices=probability_choices, null=True, max_length=20)



