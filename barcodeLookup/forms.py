from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["barcode", "name", "brand", "ingredient", "packaging", "category", "image"]
