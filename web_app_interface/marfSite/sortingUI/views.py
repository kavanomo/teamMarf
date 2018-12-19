from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Magiccards, ColourSortingFields
from django.views.generic import ListView, CreateView, UpdateView


class index(ListView):
    model = ColourSortingFields
    context_object_name = 'Colour'


def setPage(request, setName):
    setNameFormatted = setName.replace('_', ' ' )
    setCardList = Magiccards.objects.filter(setname = setNameFormatted)
    cardListFormatted = ', '.join([c.cardname for c in setCardList])
    return HttpResponse(cardListFormatted)


def userPage(request, userId):
    return HttpResponse("Hello, %s." %userId)
