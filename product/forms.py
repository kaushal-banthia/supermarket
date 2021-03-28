from django import forms
from .models import Product
from django.forms import ValidationError


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

class EditProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['quantity', 'cost_price' ,'selling_price']

