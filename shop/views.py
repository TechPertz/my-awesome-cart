from django.db.models.query import prefetch_related_objects
from django.shortcuts import render
from django.http import HttpResponse, response
from .models import Product, Contact, Orders, OrderUpdate
import json

from math import ceil, trunc

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
    thank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank' : thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')



def searchMatch(query, item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.sub_category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category = cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nslides = n//4 + ceil((n/4) - (n//4))
        if len(prod)!=0:
            allprods.append([prod, range(1, nslides), nslides])
    params = {'allprods': allprods, 'msg' : ""}
    if len(allprods) == 0:
        params = {'msg' : "Please make sure to ente relevant search query"}
    return render(request, 'shop/search.html', params)

def products(request, myid):
    product = Product.objects.filter(id = myid)
    return render(request, 'shop/products.html', {'product': product[0]})

def checkout(request):
    thank = False
    id = ""
    if request.method == "POST":
        itemsJson = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address1 = request.POST.get('address1', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=itemsJson, name=name, email=email, address=address1 + " " + address2, city = city, state = state, zip_code=zip_code, phone=phone, amount = amount)
        order.save()
        update = OrderUpdate(order_id = order.order_id, update_desc = "The Order has been placed")
        update.save()
        thank = True
        id = order.order_id
    return render(request, 'shop/checkout.html', {'thank' : thank, 'id' : id})
