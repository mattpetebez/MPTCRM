# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

# from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView

from .forms import AddSaleForm, AddMeetingForm, AddCompanyForm, AddCompanyRepresentativeForm
from .models import SalesPerson, Sale, Activity


# Create your views here.


def index(request):
    if request.user.is_authenticated():
        sales_person_list = User.objects.all().order_by('first_name')
        context = {'sales_person_list': sales_person_list}
        return render(request, 'SalesPeople/index.html', context)
    else:
        return redirect('login')


def get_sales_person(request, first_name):
    if request.user.first_name == first_name or request.user.is_superuser:
        try:
            sales_person_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        completed_sales_count = len(sales_person_in_question.sale_set.filter(sale_completed=True))
        pending_sales_count = len(sales_person_in_question.sale_set.filter(sale_completed=False))
        upcoming_meetings = (sales_person_in_question.meeting_set.filter(meeting_date__lte=datetime.now()
                                                                                           + timedelta(days=10)))
        a_month_ago = datetime.now() - timedelta(days=30)
        recent_sales = (sales_person_in_question.sale_set.filter(date_acquired__gte=a_month_ago)
                        .order_by('date_acquired')[:5])

        context = ({'sales_person_in_question': sales_person_in_question,
                    'completed_sales_count': completed_sales_count,
                    'recent_sales': recent_sales,
                    'pending_sales_count': pending_sales_count,
                    'upcoming_meetings': upcoming_meetings})
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
            post.quote_number = "MPT%d" % post.id
            post.sales_people.add(request.user)
            post.sync_sale_add()
            post.save()
            user = request.user
            success_type = "Sale"
            context = {'user': user, 'success_type': success_type}
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
            success_type = "Activity"
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form': form})
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
            post.save()
            post.sales_representative.add(request.user)

            success_type = "company"
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
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
            success_type = 'Company representative'
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
    else:
        if request.user.is_authenticated:
            form = AddCompanyRepresentativeForm()
            return render(request, 'SalesPeople/AddCompanyRepresentative.html', {'form': form})
        else:
            return HttpResponse("Need to be logged in to do that")


def show_sales(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            user_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        sales_person_in_question = SalesPerson.objects.get(user=user_in_question)

        completed_sales = user_in_question.sale_set.filter(sale_completed=True).order_by('due_date')[:5]
        pending_sales = (user_in_question.sale_set.filter(sale_completed=False)).order_by('due_date')[:5]
        context = ({'completed_sales': completed_sales, 'pending_sales': pending_sales,
                    'sales_person': sales_person_in_question, 'user_in_question': user_in_question})
        return render(request, 'SalesPeople/ViewSales.html', context)


def view_pending_sales(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            user_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        sales_person = SalesPerson.objects.get(user=user_in_question)
        pending_sales = user_in_question.sale_set.filter(sale_completed=False).order_by('due_date')
        context = ({'pending_sales': pending_sales, 'sales_person': sales_person,
                    'user_in_question': user_in_question})
        return render(request, 'SalesPeople/ViewDetailSales.htmlSales.html', context)
    else:
        return HttpResponse("What the fuck is going on")


def view_completed_sales(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            user_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        sales_person = SalesPerson.objects.get(user=user_in_question)
        sales = user_in_question.sale_set.filter(sale_completed=True).order_by('due_date')
        context = ({'pending_sales': sales, 'sales_person': sales_person,
                    'user_in_question': user_in_question})
        return render(request, 'SalesPeople/ViewDetailSales.html', context)
    else:
        return HttpResponse("What the fuck is going on")


def show_meetings(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            sales_person_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        yesterday = timezone.datetime.today() - timedelta(days=1)
        today = timezone.datetime.today()
        tomorrow = timezone.datetime.today() + timedelta(days=1)
        meetings_today = sales_person_in_question.meeting_set.filter(meeting_date__range=(yesterday, today))
        meetings_upcoming = sales_person_in_question.meeting_set.filter(meeting_date__gt=today)

        context = ({'sales_person': sales_person_in_question, 'meetings_today': meetings_today,
                    'meetings_upcoming': meetings_upcoming})
        return render(request, 'SalesPeople/ViewMeetings.html', context)


class UpdateSale(UpdateView):
    model = Sale
    fields = '__all__'
    template_name_suffix = 'Edit'

    def form_valid(self, form):
        form.save()
        success_type = "Sale"
        context = {'success_type': success_type}
        return render(self.request, 'SalesPeople/SuccessfullyEdited.html', context)


class UpdateMeeting(UpdateView):
    model = Activity
    fields = ['activity_start_date', 'company_representative', 'company', 'attended']
    exclude = ['proactive']
    template_name_suffix = 'Edit'

    def form_valid(self, form):
        form.save()
        success_type = "Activity"
        context = {'success_type': success_type}
        return render(self.request, 'SalesPeople/SuccessfullyEdited.html', context)


class DeleteMeeting(DeleteView):
    model = Activity
    template_name_suffix = "Delete"

    def get_success_url(self):
        return render(self.request, 'SalesPeople/SuccessfullyDeleted.html', context={'success_type': "Activity"})


class DeleteSale(DeleteView):
    model = Sale
    template_name_suffix = "Delete"

    def get_success_url(self):
        return render(self.request, 'SalesPeople/SuccessfullyDeleted.html', context={'success_type': "Sale"})

