from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def testMap(request):
    return HttpResponse("Hello World.");

#Delete me whenever