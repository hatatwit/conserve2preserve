from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.db.models import Count
from pyzbar.pyzbar import decode
from .models import *
from .forms import *
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

def categories(request):
    categoryDB = Categorie.objects.all()
    categories = categoryDB.annotate(products_count=Count('product'))
    context = zip(categoryDB, categories)

    return render(request, "categories.html", {"context": context})

def categoryView(request, cats):
    category = Categorie.objects.get(category=cats)
    if cats == "All Products":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__category=cats)

    return render(request, "categoryView.html", {"products": products, "category": category})

def cart(request):
    device = request.COOKIES['device']
    customer, created = Customer.objects.get_or_create(device=device)
    order, created = Order.objects.get_or_create(customer=customer)
    orderItem = order.orderitem_set.all()
    return render(request, "cart.html", {"cart": orderItem, "order": order})


def productDetail(request, barcode):
    product = Product.objects.get(barcode=barcode)
    toxicIngredient = findToxicIngredient(str(product.ingredient))
    data = upcLookupAPI(barcode)

    # Add item to the bag
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

    context = {"product": product, "data": data, "toxicIngredient": toxicIngredient, "totalIngredient": round((str(product.ingredient).count(",") + 1)/45, 2)}

    return render(request, 'productDetail.html', context)


def searchProduct(request):
    if request.method == "POST" and Product.objects.filter(name__contains=request.POST['searched']):
        return render(request, 'searchResult.html', {"items": Product.objects.filter(name__contains=request.POST['searched'])})
    else:
        return render(request, 'searchResult.html')

def scanProduct(request):
    if request.method == "POST" and request.FILES['image']:
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        img = cv2.imread('media/' + filename)
        for barcode in decode(img):
            barcode = barcode.data.decode('utf-8')
        data = upcLookupAPI(barcode)
        os.remove('media/' + filename)
        if Product.objects.filter(name__contains=data["title"]).exists():
            product = Product.objects.get(name=data["title"])
            toxicIngredient = findToxicIngredient(str(product.ingredient))
            context = {"product": product, "data": data, "toxicIngredient": toxicIngredient, "totalIngredient": round((str(product.ingredient).count(",") + 1) / 45, 2)}
            return render(request, 'scanProduct.html', context)
        else:
            return render(request, 'searchResult.html')

    else:
        return render(request, 'searchResult.html')

def upcLookupAPI(barcode):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip,deflate',
    }
    lookupURL = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc={}'.format(barcode), headers=headers)
    data = json.loads(lookupURL.text)

    productData = {}

    try:
        for data in data["items"]:
            productData["barcode"] = barcode
            productData["title"] = data["title"].split(", ", 1)[0]
            productData["description"] = data["description"]
            productData["brand"] = data["brand"]
            productData["image"] = data["images"][0]
    except:
        print("Error while collect data from UPC Lookup API.")

    return productData

def findToxicIngredient(productIngredient):
    toxicIngredientDB = ToxicIngredient.objects.all()
    toxic = []

    for item in toxicIngredientDB:
        if item.name in productIngredient:
            toxic.append(ToxicIngredient.objects.get(name=item.name))

    return toxic

def brands(request):
    brandDB = Brand.objects.all()

    return render(request, "brands.html", {"brandDB": brandDB})

def brandDetail(request, brand):
    brand = Brand.objects.get(name=brand)
    products = Product.objects.filter(brand__name=brand)
    context = {"brand": brand, "products": products}

    return render(request, "brandDetail.html", context)


def addProduct(request):
    productDB = Product.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            productForm = form.save(commit=False)
            productForm.save()
            return render(request, "index.html", {"form": form, "productDB": productDB})
    else:
        form = ProductForm()
    return render(request, "newProduct.html", {"form": form, "productDB": productDB})
