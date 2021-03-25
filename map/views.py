from django.http import HttpResponse
from django.views import generic


# Create your views here.

class MapView(generic.TemplateView):
    template_name = "map.html"

    starting_coords = [-78.510067, 38.038124]

    # TODO: Move access token and other sensitive things here

    # From : https://stackoverflow.com/questions/18232851/django-passing-variables-to-templates-from-class-based-views
    # Makes this classes global variables accessible from the templates
    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context.update({'starting_coords': self.starting_coords})
        return context
