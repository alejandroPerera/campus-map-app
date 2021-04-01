from django.views import generic
from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import ScheduleForm
import requests
import json
from .models import ClassModel, ScheduleModel
import re


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

    def __init__(self, query, coordinates, name):
        self.query = query
        self.coordinates = coordinates
        self.name = name

    @staticmethod
    def get_geo_codes(data):
        """ Transforms the json data into an array of GeoCodes """
        query = ' '.join(data.get('query'))
        results = data.get('features')
        output = []
        for result in results:
            coordinates = [result.get('center')[0], result.get('center')[1]]
            name = result.get('text')
            output.append(GeoCode(query, coordinates, name))

        return output


class MapView(generic.FormView):
    template_name = "map/map.html"
    form_class = ScheduleForm
    success_url = 'search'

    access_token = 'pk.eyJ1IjoiYS0wMiIsImEiOiJja21iMzl4dHgxeHFtMnBxc285NGMwZG5kIn0.Rl2qXrod77iHqUJ-eMbkcg'
    starting_coords = [-78.510067, 38.038124]

    # From : https://stackoverflow.com/questions/18232851/django-passing-variables-to-templates-from-class-based-views
    # Makes this classes global variables accessible from the templates
    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update({'starting_coords': self.starting_coords, 'access_token': self.access_token})
        return context


# Returns search results
def get_search_results(request):
    # Make this not stored here...
    access_token = 'pk.eyJ1IjoiYS0wMiIsImEiOiJja21iMzl4dHgxeHFtMnBxc285NGMwZG5kIn0.Rl2qXrod77iHqUJ-eMbkcg'
    starting_coords = [-78.510067, 38.038124]

    if request.method == 'POST':
        form = ScheduleForm(request.POST)  # generate the form from the data supplied
        if form.is_valid():
            base_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
            params = {'limit': 5,
                      'proximity': str(starting_coords[0]) + ',' + str(starting_coords[1]),
                      'access_token': access_token}
            # Get the data from MapBox's API
            r = requests.get(base_url + form.cleaned_data['search'] + '.json', params=params)
            # Parse that data into a more useful form
            results = GeoCode.get_geo_codes(r.json())

            return render(request, 'map/schedule.html', {'results': results})
    else:
        # Return nothing? No
        return render(request, 'map/schedule.html', {'results': []})


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


def get_class_model_results(request):
    if request.method == 'POST':
        pass
        # Looks for a series of letters, followed by a series of numbers followed by another series of numbers
        query = parse_classes(request.POST.get('search-terms'))
        class_number = query[0]
        class_mnemonic = query[1]
        course_number = query[2]
        class_section = query[3]
        results = ClassModel.objects.filter(
            class_number=class_number,
            class_mnemonic=class_mnemonic,
            course_number=course_number,
            class_section=class_section
        )

        return render(request, 'map/classes.html', {'classR': results})

    else:
        return render(request, 'map/classes.html', {})


def add_class(request):
    if request.method == 'POST':
        classList = request.POST.getlist('clicked')
        print('result:')
        print(classList)
        user = request.user
        if (user.is_authenticated):
            # if a schedule already exists
            schedule = ScheduleModel(user=user)
            schedule.save()
            for class_id in classList:
                class_to_add = ClassModel.objects.get(pk=class_id)
                schedule.courses.add(class_to_add)
                print(class_to_add)
            # response.user.schedule.add(class_to_add)
    return render(request, 'map/map.html', {})

# def update_schedule(request, user_id):
#     user = User.objects.get(pk=user_id)
#     courses = get_classModel_results(request)
#
#     user.save()
