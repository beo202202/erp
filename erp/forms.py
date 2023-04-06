from django import forms
from .models import Product, Inbound

# form.py


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'price', 'size']


class InboundForm(forms.ModelForm):
    # 입고 모델
    class Meta:
        model = Inbound
        fields = ['product', 'quantity', 'amount']
