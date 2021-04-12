from django import forms


class ScheduleForm(forms.Form):
    """ Used to create the search bar and other scheduling functionality"""
    search = forms.CharField(widget=forms.TextInput, max_length=50)
class EventForm(forms.Form):
    host = forms.CharField(widget=forms.TextInput, max_length=50)
    capacity = forms.IntegerField()
    date = forms.DateTimeField()
    # location = ScheduleForm.search
