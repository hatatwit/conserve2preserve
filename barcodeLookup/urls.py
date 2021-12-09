from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('search-result/', views.searchProduct, name="searchResult"),
    path('product/<int:barcode>/', views.productDetail, name='productDetail'),
    path('categories', views.categories, name="category"),
    path('categories/<str:cats>', views.categoryView, name="categoryView"),
    path('scan-product/', views.scanProduct, name="scanProduct"),
    path('brands/', views.brands, name="brands"),
    path('brand/<str:brand>', views.brandDetail, name="brand")
]