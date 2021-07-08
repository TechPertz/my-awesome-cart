from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

from math import ceil

# Create your views here.

def index (request):
    products = Product.objects.all()
    print(products)
    n = len(products)
    nslides = n//4 + ceil((n/4) - (n//4))
    params ={'no_of_slides': nslides, 'range': range(1, nslides),'product': products}
    return render(request,'shop/index.html')

def about (request):
    return render(request,'shop/about.html')

def contact (request):
    return HttpResponse("We are at Contact")

def tracker (request):
    return HttpResponse("We are at tracker")

def search (request):
    return HttpResponse("We are at Search")

def productview (request):
    return HttpResponse("We are at Product View")

def checkout (request):
    return HttpResponse("We are at Checkout")