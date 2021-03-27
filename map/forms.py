from profile import Profile

from django import forms


class ScheduleForm(forms.Form):
    """ Used to create the search bar and other scheduling functionality"""
    search = forms.CharField(widget=forms.TextInput, max_length=50, label="Search for buildings")

