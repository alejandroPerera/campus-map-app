from django import forms
from .models import *


class ScheduleForm(forms.Form):
    """ Used to create the search bar and other scheduling functionality"""
    search = forms.CharField(widget=forms.TextInput, max_length=50)


class MakeEventForm(forms.ModelForm):
    class Meta:
        model = EventModel
        #fields = ['title', 'location', 'date', 'capacity', 'description']
        fields = ['title', 'location', 'date', 'time', 'capacity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height: 100px;'}),
        }


class UpdateEventForm(forms.Form):
    title = forms.CharField(max_length=50)
    location = forms.CharField(max_length=200)
    #date = forms.DateTimeField()
    date = forms.DateField()
    time = forms.TimeField()
    capacity = forms.IntegerField()
    description = forms.CharField(max_length=200, widget=forms.Textarea(attrs={'style': 'height: 100px;'}))
    id = forms.IntegerField(widget=forms.HiddenInput())
