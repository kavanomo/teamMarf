from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Magiccards

def index(request):
    return HttpResponse("Hello, World.")


def setPage(request, setName):
    setNameFormatted = setName.replace('_', ' ' )
    setCardList = Magiccards.objects.filter(setname = setNameFormatted)
    cardListFormatted = ', '.join([c.cardname for c in setCardList])
    return HttpResponse(cardListFormatted)


def userPage(request, userId):
    return HttpResponse("Hello, %s." %userId)
