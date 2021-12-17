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
    recyclable = models.BooleanField(null=True)
    biodegradable = models.BooleanField(null=True)
    time = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Categorie(models.Model):
    category = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.category

class Brand(models.Model):
    name = models.CharField(max_length=100, null=True)
    intro = models.TextField(null=True)
    parentCompany = models.CharField(max_length=100, blank=True)
    crueltyFree = models.BooleanField(null=True)

    def __str__(self):
        return self.name

class ToxicIngredient(models.Model):
    name = models.CharField(max_length=150, null=True)
    info = models.TextField(null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    barcode = models.IntegerField()
    grade = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    name = models.TextField(max_length=200, null=True)
    ingredient = models.TextField(null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    packaging = models.ForeignKey(Packaging, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    image = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):

        self.grade = 100
        eachIngredient = round(((self.ingredient).count(",") + 1)/45, 2)

        # Grading bases on ingredient
        for ingredient in ToxicIngredient.objects.all():
            if ingredient.name in str(self.ingredient):
                self.grade -= eachIngredient

        # Grading bases on packaging
        if self.packaging.recyclable == False and self.packaging.biodegradable == False:
            self.grade -= 40
        elif self.packaging.recyclable == False or self.packaging.biodegradable == False:
            self.grade -= 20
        else:
            pass

        # Grading bases on company cruelty-free
        if self.brand.crueltyFree == False:
            self.grade -=15
        else:
            pass

        super(Product, self).save(*args, **kwargs)

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

    def __str__(self):
        return self.product.name
