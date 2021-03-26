from django import forms
from crispy_forms.helper import FormHelper
from django.shortcuts import reverse


class ScheduleForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput, max_length=50, label="Search for buildings")
