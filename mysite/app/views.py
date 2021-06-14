from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .scrapping import drawCityDiagram, getRoomTable, drawYardageDiagram

# Create your views here.
def index(request):
    context = {
        'CityDiagram': drawCityDiagram(),
        'RoomTable': getRoomTable(),
        'YardageDiagram': drawYardageDiagram(),
    }
    return render(request, "app/index.html", context)