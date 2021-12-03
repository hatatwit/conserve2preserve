from django.db import models
from django.contrib.auth.models import User

# Setup database for product
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    device = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.device)

class Packaging(models.Model):
    name = models.CharField(max_length=200, null=True)
    production = models.TextField(max_length=200, null=True)
    recycle = models.TextField(max_length=200, null=True)
    commonProduct = models.TextField(max_length=150, null=True)
    recyclable = models.BooleanField(null=True)
    biodegradable = models.BooleanField(null=True)
    time = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    barcode = models.IntegerField()
    grade = models.IntegerField()
    name = models.TextField(max_length=200, null=True)
    brand = models.TextField(max_length=100, null=True)
    ingredient = models.TextField(null=True)
    packaging = models.ForeignKey(Packaging, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)

    @property
    def get_cart_item(self):
        orderItem = self.orderitem_set.all()
        numItem = sum([item.quantity for item in orderItem])
        return numItem

    @property
    def get_cart_average(self):
        orderItem = self.orderitem_set.all()
        average = round(sum([item.get_grade for item in orderItem])/OrderItem.objects.count(), 1)
        return average

    def __str__(self):
        return str(self.customer)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    @property
    def get_grade(self):
        grade = self.product.grade * self.quantity
        return grade
