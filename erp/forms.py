from django import forms
from .models import Product, Inbound, Outbound

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


class OutboundForm(forms.ModelForm):
    class Meta:
        model = Outbound
        fields = ['product', 'quantity', 'amount']
        # 출고 할 때 오히려 안 좋은 것 같다...
        # widgets = {
        #     'product': forms.HiddenInput()
        # }
