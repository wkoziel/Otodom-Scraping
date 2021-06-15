from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .scrapping import drawCityDiagram, drawYardageDiagram, drawRoomDiagram, getIntroTable, drawPriceDiagram

# Create your views here.
def index(request):
    context = {
        'CityDiagram': drawCityDiagram(),
        'YardageDiagram': drawYardageDiagram(),
        'RoomDiagram': drawRoomDiagram(),
        'IntroTable': getIntroTable(),
        'PriceDiagram': drawPriceDiagram(),
    }
    return render(request, "app/index.html", context)