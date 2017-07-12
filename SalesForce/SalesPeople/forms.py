from django import forms

from .models import Sale, Meeting, Company, CompanyRepresentative


class AddSaleForm(forms.ModelForm):

    class Meta:
        model = Sale
        exclude = ['sales_people', 'sale_completed', 'date_acquired']
        fields = ('company', 'due_date', 'company_rep', 'amount', 'sale_status', 'sale_probability')
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }


class AddMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ['sales_person', 'proactive']
        # widgets = {}


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['sales_representative']


class AddCompanyRepresentativeForm(forms.ModelForm):
    class Meta:
        model = CompanyRepresentative
        fields = ['first_name', 'last_name', 'contact_number']


class EditSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = (['company', 'due_date', 'company_rep', 'sale_completed', 'sale_probability', 'sale_status'])
        exclude = ['date_acquired']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }
