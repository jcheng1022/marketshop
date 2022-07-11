from django.shortcuts import render
from django.http import HttpResponse
from .models import Item
# Create your views here.


def home (request):
    return render(request, 'home.html')

def item_index(request):
    items = Item.objects.all()
    return render(request, 'items/index.html', {'items':items})