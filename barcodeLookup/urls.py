from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cart/', views.cart, name="cart"),
    path('search-result/', views.searchProduct, name="search"),
    path('product/<int:barcode>/', views.productDetail, name='product-detail'),
    path('categories', views.categories, name="category"),
    path('categories/<str:cats>/', views.categoryView, name="category-view"),
    path('scan-product/', views.scanProduct, name="scan-product"),
    path('brands/', views.brands, name="brands"),
    path('brand/<str:brand>', views.brandDetail, name="brand"),
    path('product/add/', views.addProduct, name="add-product")
]