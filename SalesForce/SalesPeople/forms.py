from django import forms
from .models import Sale, Meeting, Company, CompanyRepresentative


class AddSaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['sales_people', 'sale_completed', 'date_acquired']

        widgets = {
            'due_date': forms.DateTimeInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }


class AddMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ['sales_person', 'proactive']


class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['sales_representative']

# class AddCompanyRepresentativeForm(forms.ModelForm):
#     class Meta:
#         model = CompanyRepresentative
