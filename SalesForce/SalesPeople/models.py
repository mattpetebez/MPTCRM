# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class SalesPerson(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    contact_number = models.CharField(max_length=10)
    total_sales_amount = models.FloatField(default=0)
    pending_sales_amount = models.FloatField(default=0)
    total_sales_count = models.IntegerField(default=0)
    pending_sales_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.first_name)

    def clear_counters(self):
        self.total_sales_amount = 0
        self.total_sales_count = 0
        self.pending_sales_amount = 0
        self.pending_sales_count = 0
        self.save()


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         SalesPerson.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.salesperson.save()


class CompanyRepresentative(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Company(models.Model):
    company_name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=10)
    company_representative = models.ForeignKey(CompanyRepresentative, null=True, blank=True)
    sales_representative = models.ManyToManyField(User)
    address = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name


class Meeting(models.Model):
    sales_person = models.ForeignKey(User)
    company_representative = models.ForeignKey(CompanyRepresentative, null=True, blank=True)
    company = models.ForeignKey(Company)
    meeting_date = models.DateTimeField('Date and time of meeting')
    proactive = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return_val = "%s: %s" % (self.company.company_name, self.sales_person.first_name)
        if self.company_representative:
            return_val = return_val + ", %s" % self.company_representative.first_name
        return return_val

#
# class Product(models.Model):
#     product_name = models.CharField(max_length=100)
#     description = models.CharField(max_length=200)
#     serial_number = models.CharField(max_length=100)
#     price = models.FloatField(null=True, blank=True)
#
#     def __str__(self):
#         return self.product_name


class SaleStatus(models.Model):
    status = models.CharField("Sale Status", max_length=12, default="Opportunity")

    def __str__(self):
        return str(self.status)


class SaleProbability(models.Model):
    probability = models.CharField("Sale Probability", max_length=10, default="Potential")

    def __str__(self):
        return str(self.probability)


class Sale(models.Model):
    amount = models.FloatField('Amount in Rands', default=0)
    date_acquired = models.DateField('Date sale was acquired')
    due_date = models.DateField('Date sale is due')
    sale_completed = models.BooleanField(default=False)
    meetings = models.ManyToManyField(Meeting, blank=True)
    sales_people = models.ManyToManyField(User, blank=True)
    company_rep = models.ForeignKey(CompanyRepresentative, blank=True, null=True)
    company = models.ForeignKey("Company", Company, null=True, blank=True)
    unique_id = models.CharField('Optional unique reminder', blank=True, null=True, max_length=20)
    status = models.ForeignKey(SaleStatus, default=SaleStatus.objects.first())
    probability = models.ForeignKey(SaleProbability, default=SaleProbability.objects.first())

    def __str__(self):
        company_name = (Company.objects.get(id=self.company_id)).company_name
        if not self.unique_id:
            return "%s: R%0.2f" % (company_name, self.amount)
        else:
            return "%s: %s" % (company_name, self.unique_id)

    def sync_sale_add(self):
        for user in self.sales_people.all():
            if self.sale_completed:
                user.salesperson.total_sales_amount += self.amount
                user.salesperson.pending_sales_amount -= self.amount
                user.salesperson.total_sales_count += 1
                user.salesperson.pending_sales_count -=1
                user.salesperson.save()
            else:
                user.salesperson.pending_sales_amount += self.amount
                user.salesperson.pending_sales_count += 1
                user.salesperson.save()









