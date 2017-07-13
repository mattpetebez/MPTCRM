from datetime import datetime

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
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'date_picker', 'id': 'date_placeholder'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'time_picker', 'id': 'time_placeholder'}))

    class Meta:

        model = Meeting
        fields = ['date', 'time', 'company_representative', 'company']
        widgets = {
            'meeting_date': forms.DateTimeInput(attrs={'class': 'date_picker', 'id': 'my_date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AddMeetingForm, self).__init__(*args, **kwargs)

        # if kwargs['instance']:
        #     self.fields['date'].initial = kwargs['instance'].meeting_date.date()
        #     self.fields['time'].initial = kwargs['instance'].meeting_date.time()

    def save(self, commit=True):
        model = super(AddMeetingForm, self).save(commit=False)
        model.meeting_date = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])

        if commit:
            model.save()

        return model


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
