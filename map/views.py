from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ScheduleForm
import requests
import json


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
        self.coordinates = (data.get('features')[0].get('center')[0], data.get('features')[0].get('center')[1])
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
            coordinates = (result.get('center')[0], result.get('center')[1])
            name = result.get('text')
            output.append(GeoCode(query, coordinates, name))

        return output


class MapView(generic.FormView):
    template_name = "map/map.html"
    form_class = ScheduleForm

    starting_coords = [-78.510067, 38.038124]
    # TODO: Make this an env variable
    access_token = 'pk.eyJ1IjoiYS0wMiIsImEiOiJja21iMzl4dHgxeHFtMnBxc285NGMwZG5kIn0.Rl2qXrod77iHqUJ-eMbkcg'

    def search_for_location(self, query) -> [GeoCode]:
        base_url = 'https://api.mapbox.com/geocoding/v5/mapbox.places/'
        params = {'limit': 5,
                  'proximity': str(self.starting_coords[0]) + ',' + str(self.starting_coords[1]),
                  'access_token': self.access_token}
        # Get the data from MapBox's API
        r = requests.get(base_url + query + '.json', params=params)
        # Parse that data into a more useful form
        return GeoCode.get_geo_codes(r.json())

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
        return render('map/schedule.html', {'results': ['Invalid Search']})
