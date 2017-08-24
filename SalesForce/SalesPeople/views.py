# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils import timezone
from django.views.generic.edit import UpdateView, DeleteView
from django import forms
from .forms import AddSaleForm, AddActivityForm, AddCompanyForm, AddCompanyRepresentativeForm, AddTeamForm,  \
    RegistrationForm, AddSaleTypeForm#, EditProfileForm
from .models import SalesPerson, Sale, Activity, SalesTeam, Goal, Company, CompanyRepresentative


# Create your views here.

def signup(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                if '@kva.co.za' in form.cleaned_data.get('email'):
                    # (User.objects.get(email=form.fields['email']).exists):
                    new_user = form.save(commit=False)
                    new_user.is_active = False
                    new_user.save()
                    new_salesperson = SalesPerson.objects.create(user_id=User.objects.get(username=form.cleaned_data.get
                    ('username')).id, contact_number=form.cleaned_data.get('contact_number'))
                    new_salesperson.save()

                    #Now need to do email confirmation of address
                    current_site = get_current_site(request)
                    uid = urlsafe_base64_encode(force_bytes(new_user.id))
                    token = account_activation_token.make_token(new_user)
                    print('Token: %s\nuid: %s\n' % (token, uid))
                    message = render_to_string('registration/AccountVerification.html', {
                        'new_user': new_user,
                        'domain': current_site.domain,
                        'uid': uid,
                        'token': token,
                    })
                    mail_subject = 'Activate your CRM account'
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    email.send()
                    return HttpResponse('Please verify your account via the email sent to you. <a href=\'/login\'> Go back</a>')

                else:
                        context = {'name': form.cleaned_data.get('first_name'), 'success_type': False}
                        return render(request, 'registration/SignupFailed.html', context)
            else:
                messages.error(request, "Error")
                return render(request, 'SalesPeople/template.html', {'form': form})
        else:
            form = RegistrationForm()
            return render(request, 'registration/signup.html', {'form': form})
    else:
        return render(request, 'SalesPeople/Errors/SignupWhileLoggedIn.html')


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if User is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        context = {'name': user.first_name, 'username': user.username, 'success_type': 'User'}
        return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
    else:
        return HttpResponse('Your token validation was failed. Are you sure you\'re using a valid token?')


def view_team(request, pk):

    team = SalesTeam.objects.get(id=pk)
    team_members = team.team_members.all()
    team_member_profiles = []
    for person in team_members:
        temp = (person, person.salesperson)
        team_member_profiles.append(temp)

    team_leader = (team.team_leader, team.team_leader.salesperson)

    if request.user.is_superuser or request.user.id == team.team_leader_id:

        context = {'team_leader': team_leader, 'team_members': team_member_profiles,
                   'team_sales': team.team_sales.order_by('date_added')[:5]}
        return render(request, 'SalesPeople/TeamLeaderViews/ViewTeam.html', context)
    else:
        return HttpResponse("Only the team leader, %s, or administrator can view this team."
                            % team.team_leader.first_name)


def index(request):
    if request.user.is_authenticated():
        users_salesperson = SalesPerson.objects.get(user=request.user)
        if request.user.is_superuser:
            teams = SalesTeam.objects.all()
            context = {'teams': teams}
            return render(request, 'SalesPeople/AdminViews/ViewTeams.html', context)

        elif users_salesperson.team_leader:
            return view_team(request, request.user.team_leader_user.get().id)
        else:
            return redirect('%s/' % request.user.first_name)
    else:
        return redirect('login')


def view_all_teams(request):
    if request.user.is_authenticated and request.user.is_superuser:
        teams = SalesTeam.objects.all()
        return render(request, 'SalesPeople/AdminViews/ViewTeams.html', {'teams': teams})


def individual_dashboard(request, first_name):
    if request.user.first_name == first_name or request.user.is_superuser:
        try:
            sales_person_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        completed_sales_count = (len(sales_person_in_question.prime_salesperson.filter(sale_completed=True))
                                 + len(sales_person_in_question.secondary_salespeople.filter(sale_completed=True)))

        pending_sales_count = (len(sales_person_in_question.prime_salesperson.filter(sale_completed=False))+
                               len(sales_person_in_question.secondary_salespeople.filter(sale_completed=False)))

        upcoming_activities = sales_person_in_question.activity_set.filter(activity_start_date__range=((timezone.now() -
                                                                           timedelta(days=5)),
                                                                           (timezone.now() + timedelta(days=10))))

        current_goals = sales_person_in_question.goal_set.filter()

        recent_sales = (list(sales_person_in_question.prime_salesperson.all()) +
                        list(sales_person_in_question.secondary_salespeople.all()))[:5]

        context = ({'sales_person_in_question': sales_person_in_question,
                    'completed_sales_count': completed_sales_count,
                    'recent_sales': recent_sales,
                    'pending_sales_count': pending_sales_count,
                    'upcoming_activities': upcoming_activities,
                    'current_goals': current_goals})
        return render(request, 'SalesPeople/ViewTemplates/IndividualDashboard.html', context)
    else:
        return HttpResponse("%s, you cannot view %s's profile." % (request.user.first_name, first_name))


def get_sale(request, company_name, first_name):  # Need to build a list of the people related to one item
    return HttpResponse("Company: %s sale to follow for salesperson %s." % (company_name, first_name))


def add_sale(request, first_name):

    if request.method == "POST":
        form = AddSaleForm(request.POST)
        if form.is_valid():
            new_sale = form.save(commit=False)
            new_sale.sale_completed = False
            new_sale.date_added = timezone.now().date()
            new_sale.prime_salesperson = User.objects.get(id=request.user.id)
            new_sale.company = new_sale.company_rep.company_set.get()
            new_sale.save()
            new_sale.quote_number = "MPT%d" % new_sale.id
            new_sale.save()
            user = request.user
            success_type = "Sale"
            context = {'user': user, 'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form': form})

    else:
        if request.user.is_authenticated:
            if request.user.first_name == first_name:
                form = AddSaleForm()

                form.fields['other_salespeople'].queryset = User.objects.all().exclude(id=request.user.id)
                context = {'form': form}

                return render(request, 'SalesPeople/AddTemplates/AddSale.html', context)
            else:
                return HttpResponse("%s, you cannot add sales to %s's account." % (request.user.first_name, first_name))
        else:
            return HttpResponse("You have to be logged in to do that.")


def add_sale_type(request, first_name):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddSaleTypeForm(request.POST)
            if form.is_valid():
                new_sale_type = form.save()
                return render(request, 'SalesPeople/SuccessfullyAdded.html', {'success_type':"Sale Type"})
        else:
            form = AddSaleTypeForm()
            return render(request, 'SalesPeople/AddTemplates/AddSaleType.html', {'form':form})


def add_activity(request, first_name):
    if request.method == "POST":
        form = AddActivityForm(request.POST)
        if form.is_valid():
            # Save for all instances
            post = form.save(commit=False)
            if request.user.is_superuser or request.user.salesperson.team_leader:
                    post.save()
            else:
                post.sales_person = request.user
                post.proactive = True
                post.save()
            # Now, need to add activity to the relevant sales
            # related_sale = form.cleaned_data['related_opportunity']
            # related_sale.activities.add(post)
            post.proactive = True
            post.save()
            success_type = "Activity"
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form': form})
    else:
        # Check if oke is logged in
        if request.user.is_authenticated:
            # Now, need three checks: If just user, if team leader or if super user
            form = None
            # User is admin superuser
            if request.user.is_superuser:
                form = AddActivityForm()
                # User is team leader
            elif request.user.salesperson.team_leader:
                team_id = request.user.team_leader_user.get().id
                form = AddActivityForm(sales_team_id=team_id)
            # User is just a dude
            else:
                form = AddActivityForm(sales_person_id=request.user.id)

            return render(request, 'SalesPeople/AddTemplates/AddActivity.html', {'form': form})



            #     form = AddActivityForm(sales_person_id=request.user.id)
            #     return render(request, 'SalesPeople/AddTemplates/AddActivity.html', {'form': form})
            # elif request.user.is_superuser:
            #     form = AddActivityForm()
            #     return render(request, 'SalesPeople/AddTemplates/AddActivity.html', {'form': form})
            # else:
            #     return HttpResponse("%s, you cannot add an activity for %s" % (request.user.first_name, first_name))


def add_company(request, first_name):
    if request.method == "POST":
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            post.sales_representative.add(request.user)

            success_type = "Company"
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
        else:
            messages.error(request, "Error")
            return render(request, 'SalesPeople/template.html', {'form': form})
    else:
        if request.user.is_authenticated:
            if request.user.first_name == first_name:
                form = AddCompanyForm()
                return render(request, 'SalesPeople/AddTemplates/AddCompany.html', {'form': form})
            else:
                return HttpResponse("%s, you cannot add a meeting for %s" % (request.user.first_name, first_name))


def add_company_representative(request, first_name):
    if request.method == "POST":
        form = AddCompanyRepresentativeForm(request.POST)
        if form.is_valid():
            new_rep = form.save()
            company = Company.objects.get(company_name=form.cleaned_data['company'].company_name)
            company.company_representative.add(new_rep)
            success_type = 'Company representative'
            context = {'success_type': success_type}
            return render(request, 'SalesPeople/SuccessfullyAdded.html', context)
    else:
        if request.user.is_authenticated:
            form = AddCompanyRepresentativeForm()
            return render(request, 'SalesPeople/AddTemplates/AddCompanyRepresentative.html', {'form': form})
        else:
            return HttpResponse("Need to be logged in to do that")


def show_sales(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            user_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        sales_person_in_question = SalesPerson.objects.get(user=user_in_question)
        pending_sales = Sale.objects.filter(Q(prime_salesperson=user_in_question) | Q(other_salespeople=user_in_question),
                                            sale_completed=False).distinct()
        completed_sales = Sale.objects.filter(Q(prime_salesperson=user_in_question) | Q(other_salespeople=user_in_question),
                                              sale_completed=True).distinct()
        context = ({'completed_sales': completed_sales, 'pending_sales': pending_sales,
                    'sales_person': sales_person_in_question, 'user_in_question': user_in_question})
        return render(request, 'SalesPeople/ViewTemplates/ViewSales.html', context)


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
        return render(request, 'SalesPeople/ViewTemplates/ViewDetailSales.html', context)
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
        return render(request, 'SalesPeople/ViewTemplates/ViewDetailSales.html', context)
    else:
        return HttpResponse("What the fuck is going on")


def show_activities(request, first_name):
    if (request.user.first_name == first_name and request.user.is_authenticated) or request.user.is_superuser:
        try:
            sales_person_in_question = User.objects.get(first_name=first_name)
        except SalesPerson.DoesNotExist:
            raise Http404("Sales person does not exist")
        yesterday = timezone.datetime.today().replace(hour=0, second=0)
        today = timezone.datetime.today().replace(hour=0, second=0)+timedelta(days=1)
        activities_today = sales_person_in_question.activity_set.filter(activity_start_date__range=(yesterday, today))
        activities_upcoming = sales_person_in_question.activity_set.filter(activity_start_date__gt=today)

        context = ({'sales_person': sales_person_in_question, 'activities_today': activities_today,
                    'activities_upcoming': activities_upcoming})
        return render(request, 'SalesPeople/ViewTemplates/ViewActivities.html', context)


# def edit_profile(request):
#     if request.method == "POST":
#         form = EditProfileForm(request.POST, request)
#         if form.is_valid():
#             profile = form.save(commit=False)


class UpdateSale(UpdateView):
    model = Sale
    fields = ['prime_salesperson',  'order_value', 'quoted_value', 'due_date', 'probability', 'status',
              'sale_completed', 'activities', 'other_salespeople', 'company_rep', 'company', 'consulting_company',
              'consultant', 'unique_id', 'sale_description', 'margin',  'sale_types', 'currency',
              'rate_of_exchange']
    # exclude = ['quote_number', 'date_added', 'prime_salesperson', 'date_sale_completed']
    template_name = 'SalesPeople/EditTemplates/EditSale.html'

    def form_valid(self, form):
        form.save()
        success_type = "Sale"
        context = {'success_type': success_type}
        return render(self.request, 'SalesPeople/SuccessfullyEdited.html', context)


class DeleteSale(DeleteView):
    model = Sale
    template_name = 'SalesPeople/DeleteTemplates/DeleteSale.html'
    success_url = 'SalesPeople/SuccessfullyDeleted.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return render(request, 'SalesPeople/SuccessfullyDeleted.html', context={'success_type': "Sale"})


class UpdateActivity(UpdateView):
    model = Activity
    fields = ['activity_start_date', 'company_representative', 'company', 'completed', 'activity', 'activity_type',
              'activity_end_date', 'description', 'title']
    exclude = ['proactive']
    template_name = 'SalesPeople/EditTemplates/EditMeeting.html'

    def form_valid(self, form):
        form.save()

        context = {'success_type': "Activity"}
        return render(self.request, 'SalesPeople/SuccessfullyEdited.html', context)


class DeleteActivity(DeleteView):
    model = Activity
    template_name = 'SalesPeople/DeleteTemplates/DeleteActivity.html'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return render(request, 'SalesPeople/SuccessfullyDeleted.html', context={'success_type': "Activity"})


def add_team(request, first_name):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddTeamForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                post.date_added = timezone.now()
                return render(request, 'SalesPeople/SuccessfullyAdded.html', {'success_type': "Team"})
            else:
                messages.error(request, "Error")
                return render(request, 'SalesPeople/AdminViews/AddTeam.html', {'form':form})
        else:
            if request.user.is_authenticated:
                if request.user.is_superuser:
                    form = AddTeamForm()
                    potential_users = User.objects.filter(team_member_set=None, team_leader_user=None)
                    committed_users = User.objects.filter(team_member_set__isnull=False, team_leader_user__isnull=False)
                    return render(request, 'SalesPeople/AdminViews/AddTeam.html',
                                  {'form': form, 'possible_members': potential_users, 'already_taken': committed_users})
                else:
                    return HttpResponse("You are not privileged to add teams. "
                                        "Please contact an administrator to add a team")

    else:
        return HttpResponse('Need to be an admin to add teams')


def update_team(request, pk):
    instance = SalesTeam.objects.get(id=pk)
    form = AddTeamForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        teams = SalesTeam.objects.all().exclude(branch_name=form.cleaned_data.get('branch_name'))
        new_members = SalesTeam.objects.get(branch_name=form.cleaned_data.get('branch_name')).team_members.all()

        for team in teams:
            for member in new_members:
                team.team_members.remove(member)
                member.save()
            team.save()

        return render(request, 'SalesPeople/SuccessfullyEdited.html', {'success_type':"Team"})

    return render(request, 'SalesPeople/AdminViews/EditTeam.html', {'form': form})
