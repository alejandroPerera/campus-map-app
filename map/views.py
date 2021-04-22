from django.views import generic
from django.shortcuts import render
from .forms import ScheduleForm, MakeEventForm
import requests
import json
from .models import ClassModel, EventModel
import re
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.

class GeoCode:
    """
    Data format:
    {
    type: ...,
    query: [What you searched for],
    features: [{lots of data}]
    attribution: copyright notice. This data cannot be retained?
    }
    """

    def __init__(self, response):
        data = json.load(response)
        self.query = data.get('query')
        self.coordinates = [data.get('features')[0].get('center')[0], data.get('features')[0].get('center')[1]]
        self.name = data.get('features')[0].get('text')
        self.location = data.get('features')[0].get('place_name')

    def __init__(self, query, coordinates, name, location_name):
        self.query = query
        self.coordinates = coordinates
        self.name = name
        self.location_name = location_name

    @staticmethod
    def get_geo_codes(data):
        """ Transforms the json data into an array of GeoCodes """
        query = ' '.join(data.get('query'))
        results = data.get('features')
        output = []
        for result in results:
            coordinates = [result.get('center')[0], result.get('center')[1]]
            name = result.get('text')
            location_name = result.get('place_name')
            output.append(GeoCode(query, coordinates, name, location_name))

        return output


class SearchResult:

    def __init__(self, class_name, class_room, class_loc_coords, class_id, signed_in, in_schedule):
        self.class_name = class_name
        self.class_room = class_room
        self.class_loc_coords = class_loc_coords
        self.class_id = class_id
        self.signed_in = signed_in
        if not self.signed_in:
            self.in_schedule = False
        else:
            self.in_schedule = in_schedule

    def __str__(self):
        return self.class_name


class MapView(generic.FormView):
    template_name = "map/map.html"
    form_class = ScheduleForm

    access_token = 'pk.eyJ1IjoiYS0wMiIsImEiOiJja21iMzl4dHgxeHFtMnBxc285NGMwZG5kIn0.Rl2qXrod77iHqUJ-eMbkcg'
    starting_coords = [-78.510067, 38.038124]

    # From : https://stackoverflow.com/questions/18232851/django-passing-variables-to-templates-from-class-based-views
    # Makes this classes global variables accessible from the templates
    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update({'starting_coords': self.starting_coords, 'access_token': self.access_token})
        context['eventsList'] = EventModel.objects.all()  # created a variable that map.html can see
        return context


# Returns search results
def get_search_results(query):
    # Make this not stored here...
    access_token = 'pk.eyJ1IjoiYS0wMiIsImEiOiJja21iMzl4dHgxeHFtMnBxc285NGMwZG5kIn0.Rl2qXrod77iHqUJ-eMbkcg'
    starting_coords = [-78.510067, 38.038124]

    base_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
    params = {'limit': 5,
              'proximity': str(starting_coords[0]) + ',' + str(starting_coords[1]),
              'bbox': '-78.526434,38.028392,-78.475622,38.055975',
              'access_token': access_token}
    # Get the data from MapBox's API
    r = requests.get(base_url + query + '.json', params=params)
    # Parse that data into a more useful form
    return GeoCode.get_geo_codes(r.json())


def parse_classes(search_input):
    """ Returns an array of the [Class number, class mnemonic, course number, class section] with None
    if that part could not be found """
    # Looks for a series of letters, followed by a series of numbers followed by another series of numbers
    result = re.search('[0-9]*\s*[a-zA-Z]*\s*[0-9]*\s*[0-9]*', search_input)
    if result:
        output = [None, None, None, None]
        array = result.group().split()
        for element in array:
            if element.isalpha() and 2 <= len(element) <= 4:  # This must be the mnemonic
                element = element.upper()
                mnemonic = ClassModel.objects.filter(class_mnemonic=element)
                if mnemonic.exists():
                    output[1] = element
            else:  # Must be a number
                if len(element) == 5:  # Must be the class number
                    output[0] = element
                if len(element) == 4:  # Must be the course number
                    output[2] = element
                if len(element) <= 3:  # Must be the section number
                    output[3] = element

        return output
    else:
        return [None, None, None, None]


def get_class_search_results(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)  # generate the form from the data supplied

        if form.is_valid():
            query = parse_classes(form.cleaned_data['search'])
            class_number = query[0]
            class_mnemonic = query[1]
            course_number = query[2]
            class_section = query[3]

            if query == [None, None, None, None]:
                results = get_search_results(form.cleaned_data['search'])

                return render(request, 'map/locations.html', {'results': results})

            # Creates a filter chain from the results of the parsing. Should strip out
            # anything not relevant
            results = ClassModel.objects
            if class_number is not None:
                results = results.filter(class_number=class_number)
            if class_mnemonic is not None:
                results = results.filter(class_mnemonic=class_mnemonic)
            if course_number is not None:
                results = results.filter(course_number=course_number)
            if class_section is not None:
                results = results.filter(class_section=class_section)

            output = []
            for r in results:
                # Don't use the search API if we know it won't return anything
                if r.class_room != 'Web-Based Course-No class mtgs' \
                        and r.class_room != 'Web-Based Course' \
                        and r.class_room != 'TBA':
                    # Searches for the building after removing any room numbers
                    search_results = get_search_results(re.sub('\d', '', r.class_room))
                    if len(search_results) != 0:
                        coords = search_results[0].coordinates
                    else:
                        coords = None
                else:
                    coords = None

                # Check if it's in the user's schedule
                user = request.user
                if user.is_authenticated:
                    in_schedule = r in user.schedule.all()
                else:
                    in_schedule = False

                output.append(
                    SearchResult(r.__str__(), r.class_room, coords, r.class_number, user.is_authenticated, in_schedule))

            return render(request, 'map/classes.html', {'classR': output})

    else:
        return render(request, 'map/classes.html', {'classR': []})


def add_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class-id')
        user = request.user
        print(class_id)
        if user.is_authenticated:
            class_to_add = ClassModel.objects.get(class_number=class_id)
            user.schedule.add(class_to_add)
            schedule = user.schedule.all()
            return render(request, 'map/user_schedule.html', {'schedule': schedule})

        return render(request, 'map/user_schedule.html', {'schedule': []})

    return render(request, 'map/user_schedule.html', {'schedule': []})


def remove_class(request):
    if request.method == 'POST':
        class_id = request.POST.get('class-id')
        user = request.user
        if user.is_authenticated:
            class_to_remove = ClassModel.objects.get(class_number=class_id)
            user.schedule.remove(class_to_remove)
            schedule = user.schedule.all()
            return render(request, 'map/user_schedule.html', {'schedule': schedule})

        return render(request, 'map/user_schedule.html', {'schedule': []})

    return render(request, 'map/user_schedule.html', {'schedule': []})


def user_created_event(request):
    if request.method == 'POST':
        user = request.user
        event_form = MakeEventForm(request.POST)
        if user.is_authenticated and event_form.is_valid():
            entry = event_form.save(commit=False)  # Don't save to the database just yet
            entry.host = user  # Tie the host to this user
            # Ignore the attendees they are set later
            entry.save()  # Save to the database
            event_form.save_m2m()  # Needs to be called if commit = False
            return render(request, 'map/event.html', {'success': True})

    return render(request, 'map/event.html', {'success': False})


def attend_event(request):
    if request.method == 'POST':
        user = request.user
        event_id = request.POST.get('event')
        event_to_attend = EventModel.objects.get(pk=event_id)
        # checks if already attending event and if host tries to attend own event
        if event_to_attend.host != user and event_to_attend not in user.attendees.all():
            user.attendees.add(event_to_attend)  # link user and event
            event_to_attend.numberOfAttendees += 1  # update attendance
            event_to_attend.save()

    return render(request, 'map/event_list.html', {'eventsList': EventModel.objects.all()})


def cancel_event(request):
    if request.method == 'POST':
        user = request.user
        event_id = request.POST.get('event')
        event_to_attend = EventModel.objects.get(pk=event_id)
        user.attendees.remove(event_to_attend)  # unlink user and event
        event_to_attend.numberOfAttendees -= 1  # update attendance
        event_to_attend.save()

    return render(request, 'map/event_list.html', {'eventsList': EventModel.objects.all()})


def remove_event_from_list(request):
    if request.method == 'POST':
        event_id = request.POST.get('event')
        user = request.user
        if user.is_authenticated:
            EventModel.objects.get(pk=event_id).delete()

        return render(request, 'map/event_list.html', {'eventsList': EventModel.objects.all()})

    return render(request, 'map/event_list.html', {'eventsList': EventModel.objects.all()})


def get_event_list(request):
    print(EventModel.objects.all())
    return render(request, 'map/event_list.html', {'eventsList': EventModel.objects.all()})

def show_schedule_page(request):
    return render(request,'map/schedule_page.html')

def show_events_page(request):
    return render(request,'map/events_page.html', {'eventsList': EventModel.objects.all()})