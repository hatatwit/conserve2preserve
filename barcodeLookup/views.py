from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pyzbar.pyzbar import decode
from .models import *
import requests
import cv2
import json
import os

def index(request):
    try:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    except:
        print("Error cookies")
    productDB = Product.objects.all()
    return render(request, "index.html", {"productDB": productDB})

def cart(request):
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem = order.orderitem_set.all()
    return render(request, "cart.html", {"cart": orderItem, "order": order})

def productDetail(request, barcode):
    item = Product.objects.get(barcode=barcode)
    if request.method == 'POST':
        newItem = Product.objects.get(barcode=barcode)
        try:
            device = request.COOKIES['device']
            customer, created = Customer.objects.get_or_create(device=device)
        except:
            print("Error customer")
        order, created = Order.objects.get_or_create(customer=customer)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=newItem)
        orderItem.save()
        return redirect("cart")

    return render(request, 'productDetail.html', {"item": item})

def scanProduct(request):
    if request.method == "POST" and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        img = cv2.imread('media/' + filename)
        for barcode in decode(img):
            barcode = barcode.data.decode('utf-8')
        productDetail = upcLookupAPI(barcode)
        #os.remove('media/' + filename)
        return render(request, 'productDetail.html', {"barcode": barcode, "productDetail": productDetail})
    else:
        return render(request, 'productDetail.html')

def upcLookupAPI(search):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
    }

    if search.isdecimal():
        lookupURL = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(search), headers=headers)
        data = json.loads(lookupURL.text)
    else:
        searchURL = requests.get('https://api.upcitemdb.com/prod/trial/search?s={}&match_mode=1&type=product'.format(search.replace(" ", "%")), headers=headers)
        data = json.loads(searchURL.text)

    upcLookupData = {}

    for item in data["items"]:
        upcLookupData["title"] = item["title"].split(", ", 1)[0]
        upcLookupData["description"] = item["description"]
        upcLookupData["brand"] = item["brand"]
        upcLookupData["category"] = item["category"]
        upcLookupData["image"] = item["images"][0]


    return upcLookupData





