from django.http import HttpResponse
from django.views import generic


# Create your views here.

class MapView(generic.TemplateView):
    template_name = "map.html"
