from django.db.models.query import prefetch_related_objects
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders

from math import ceil

# Create your views here.


def index(request):
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n = len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        allprods.append([prod, range(1, nslides), nslides])
    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def products(request, myid):
    # fetch the ptoduct using id
    product = Product.objects.filter(id = myid)
    return render(request, 'shop/products.html', {'product': product[0]})

def checkout(request):
    thank = False
    id = ""
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=itemsJson, name=name, email=email, address=address1 + " " + address2, city = city, state = state, zip_code=zip_code, phone=phone)
        order.save()
        thank = True
        id = order.order_id
    return render(request, 'shop/checkout.html', {'thank' : thank, 'id' : id})
