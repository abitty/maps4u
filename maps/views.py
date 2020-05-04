from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def AllMaps(request):
    return HttpResponse("Коллекция старинных карт")