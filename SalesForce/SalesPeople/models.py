# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    sales_representative = models.ForeignKey(User, null=True, blank=True)
    address = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name


class Meeting(models.Model):
    sales_person = models.ForeignKey(User)
    company_representative = models.ForeignKey(CompanyRepresentative, null=True, blank=True)
    company = models.ForeignKey(Company)
    meeting_date = models.DateTimeField('Date and time of meeting')
    proactive = models.BooleanField(default=False)

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
#

class Sale(models.Model):
    amount = models.FloatField(default=0)
    date_acquired = models.DateField('Date sale was acquired')
    due_date = models.DateField('Date sale is due')
    sale_completed = models.BooleanField(default=False)
    meetings = models.ManyToManyField(Meeting, blank=True)
    sales_people = models.ManyToManyField(User, blank=True)
    company_rep = models.ForeignKey(CompanyRepresentative, blank=True, null=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    def __str__(self):
        company_name = (Company.objects.get(id=self.company_id)).company_name
        return "%s: R%0.2f" % (company_name, self.amount)

