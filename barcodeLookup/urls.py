from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('product/<int:barcode>/', views.productDetail, name='productDetail'),
]