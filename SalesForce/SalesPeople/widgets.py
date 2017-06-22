from django.contrib.admin import widgets as Widgets
from django import forms


class CustomAdminSplitDateTime(Widgets.AdminSplitDateTime):

    def __init__(self, attrs=None):
        widgets = [Widgets.AdminDateWidget, Widgets.AdminTimeWidget(attrs=None, format='%I:%M %p')]
        forms.MultiWidget.__init__(self, widgets, attrs)
