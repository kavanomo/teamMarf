from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. This is my first web app and will form the basis of our FYDP's interface.")
