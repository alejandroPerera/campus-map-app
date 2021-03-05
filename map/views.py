from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def test_map(request):
    return HttpResponse("Hello World.")
