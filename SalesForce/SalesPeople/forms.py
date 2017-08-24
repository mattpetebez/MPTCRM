from datetime import datetime

from django import forms
from django.db.models import Q
from .models import Sale, Activity, Company, CompanyRepresentative, SalesTeam, SaleType
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .widgets import AddAnotherWidgetWrapper


class RegistrationForm(UserCreationForm):

    contact_number = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=20, label='First Name')
    last_name = forms.CharField(max_length=20, label='Surname')
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'contact_number']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email address is not unique.')
        elif 'kva.co.za' not in email:
            raise forms.ValidationError(u'Email address must be a \"@kva.co.za\" address.')
        return email

#
# class EditProfileForm(forms.ModelForm):
#
#         # contact_number = forms.CharField(max_length=10, initial=request.user)
#
#         class Meta:
#             model = User
#             exclude = ['username', 'password']
#             # fields = ['email', 'contact_number', 'name']
#
#         # def __init__(self, *ars, **kwargs):
#         #     super(EditProfileForm, self).__init__(*args, **kwargs)
#         #     self.fields


class AddSaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        fields = ['other_salespeople', 'due_date', 'sale_description', 'unique_id', 'quoted_value', 'order_value', 'status',
                  'probability', 'company_rep', 'consultant', 'margin', 'currency', 'sale_types', 'rate_of_exchange']
        exclude = ['date_added', 'date_sale_completed', 'sale_completed', "activities", 'consulting_company', 'company']
        widgets = {
            'due_date': forms.DateInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddSaleForm, self).__init__(*args, **kwargs)

        self.fields['company_rep'].required = True


class AddSaleTypeForm(forms.ModelForm):

    class Meta:
        model = SaleType
        fields = ['sale_type', 'sale_description']


class AddActivityForm(forms.ModelForm):
    start_date_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'start_date_picker', 'id': 'start_date_placeholder'}))
    start_date_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'start_time_picker', 'id': 'start_time_placeholder'}))
    end_date_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'end_date_picker', 'id': 'date_placeholder'}))
    end_date_time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'end_time_picker', 'id': 'time_placeholder'}))

    class Meta:
        model = Activity
        fields = ['start_date_date', 'start_date_time', 'end_date_date', 'end_date_time', 'company_representative',
                  'company', 'consultant', 'consulting_company', 'title', 'description', 'activity_type', 'action',
                  'sales_person']

    def __init__(self, *args, **kwargs):
        sales_person_id = None
        sales_team_id = None

        if 'sales_person_id' in kwargs:
            sales_person_id = kwargs.pop('sales_person_id')

        if 'sales_team_id' in kwargs:
            sales_team_id = kwargs.pop('sales_team_id')

        super(AddActivityForm, self).__init__(*args, **kwargs)

        self.fields['company_representative'].required=False
        self.fields['consultant'].required=False
        self.fields['consulting_company'].required=False
        # Case of just a person adding an activity for themselves, needs only their relevant sales
        if sales_person_id:
            sales_person = User.objects.get(id=sales_person_id)
            sales_person_sales = Sale.objects.filter(Q(prime_salesperson=sales_person) |
                                                     Q(other_salespeople=sales_person))
            self.fields['related_opportunity'] = forms.ModelChoiceField(
                required=False,
                queryset=sales_person_sales,
                widget=forms.Select()
            )
        # The case of a team leader adding activities for team members, has to choose related opportunity and
        #  team member
        elif sales_team_id:

            sales_team_name = SalesTeam.objects.get(id=sales_team_id)
            sales_team = list(sales_team_name.team_members.all()).append(sales_team.team_leader.get())

            self.fields['sales_person'] = forms.ModelChoiceField(
                required=True,
                queryset=sales_team,
                widget=forms.Select()
            )
            # Now, need all the sales related to that team.

            sales_team_sales = Sale.objects.filter(Q(prime_salesperson__in=sales_team) |
                                                   Q(other_salespeople__in=sales_team)).distinct()
            self.fields['related_opportunity'] = forms.ModelChoiceField(
                required=False,
                queryset=sales_team_sales,
                widget=forms.Select()
            )

        # Case of a superuser (admin) adding a task for anyone
        else:

            self.fields['sales_person'] = forms.ModelChoiceField(
                required=True,
                queryset=User.objects.all(),
                widget=forms.Select()
            )

            self.fields['related_opportunity'] = forms.ModelChoiceField(
                required=False,
                queryset=Sale.objects.all(),
                widget=forms.Select(),
            )

    def save(self, commit=True):
        model = super(AddActivityForm, self).save(commit=False)
        model.activity_start_date = datetime.combine(self.cleaned_data['start_date_date'],
                                                     self.cleaned_data['start_date_time'])
        model.activity_end_date = datetime.combine(self.cleaned_data['end_date_date'],
                                                   self.cleaned_data['end_date_time'])

        if commit:
            model.save()

        return model


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['sales_representative']

    def __init__(self, *args, **kwargs):
        super(AddCompanyForm, self).__init__(*args, **kwargs)

        self.fields['company_representative'].required = False


class AddCompanyRepresentativeForm(forms.ModelForm):
    company = forms.ModelChoiceField(Company.objects.all(), required=True)

    class Meta:
        model = CompanyRepresentative
        fields = ['first_name', 'last_name', 'contact_number']


class EditSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (['company', 'due_date', 'company_rep', 'sale_completed', 'sale_types', 'margin', 'sale_description',
                   'consultant', ])
        exclude = ['date_added']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditSaleForm, self).__init__(*args, **kwargs)

        self.fields['company'].required = True


class AddTeamForm(forms.ModelForm):
    class Meta:
        model = SalesTeam
        fields = (['team_leader', 'team_members', 'branch_name'])
        exclude = ['date_added']
