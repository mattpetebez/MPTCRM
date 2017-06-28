# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import SalesPerson, Sale, Company, CompanyRepresentative, Meeting
from .forms import AddSaleForm, AddMeetingForm, AddCompanyForm, AddCompanyRepresentativeForm
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
# Create your views here.


def index(request):
    if request.user.is_authenticated():
        sales_person_list = User.objects.order_by()
        context = {'sales_person_list': sales_person_list}
        return render(request, 'SalesPeople/index.html', context)
    else:
        return redirect('login')


def get_sales_person(request, first_name):
    if request.user.first_name == first_name:
        try:
            sales_person_in_question = request.user.salesperson
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        sales_person_sales = request.user.sale_set.all()
        context = {'sales_person_in_question': sales_person_in_question, 'sales_person_sales': sales_person_sales}
        return render(request, 'SalesPeople/SalespersonDetail.html', context)
    else:
        return HttpResponse("%s, you cannot view %s's profile." % (request.user.first_name, first_name))


def get_sale(request, company_name, first_name):  # Need to build a list of the people related to one item
    return HttpResponse("Company: %s sale to follow for salesperson %s." % (company_name, first_name))


def add_sale(request, first_name):
    if request.method == "POST":
        form = AddSaleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sale_completed = False
            post.date_acquired = timezone.now().date()
            post.save()
            post.sales_people.add(request.user)
            post.sync_sale_add()
            user = request.user
            success_type = "Sale"
            context = {'user':user, 'success_type':success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
    else:
        if request.user.is_authenticated:
            if request.user.first_name == first_name:
                form = AddSaleForm()
                return render(request, 'SalesPeople/AddSale.html', {'form': form})
            else:
                return HttpResponse("%s, you cannot add sales to %s's account." % (request.user.first_name, first_name))
        else:
            return HttpResponse("You have to be logged in to do that.")


def add_meeting(request, first_name):
    if request.method == "POST":
        form = AddMeetingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sales_person = request.user
            post.proactive = True
            post.save()
            return HttpResponse("Meeting successfully saved.")
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form':form})
    else:
        if request.user.is_authenticated:
            if request.user.first_name == first_name:
                form = AddMeetingForm()
                return render(request, 'SalesPeople/AddMeeting.html', {'form': form})
            else:
                return HttpResponse("%s, you cannot add a meeting for %s" % (request.user.first_name, first_name))


def add_company(request, first_name):
    if request.method == "POST":
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.sales_representative.add(request.user)
            post.save()
            return HttpResponse("Company successfully saved.")
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form': form})
    else:
        if request.user.is_authenticated:
            if request.user.first_name == first_name:
                form = AddCompanyForm()
                return render(request, 'SalesPeople/AddCompany.html', {'form': form})
            else:
                return HttpResponse("%s, you cannot add a meeting for %s" % (request.user.first_name, first_name))


def add_company_representative(request, first_name):
    if request.method == "POST":
        form = AddCompanyRepresentativeForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return HttpResponse("Company Representative %s %s added successfully" % (post.first_name, post.last_name))
    else:
        if request.user.is_authenticated:
            form = AddCompanyRepresentativeForm()
            return render(request, 'SalesPeople/AddCompanyRepresentative.html', {'form': form})
        else:
            return HttpResponse("Need to be logged in to do that")


