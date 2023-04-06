from django import forms
from .models import Product

# form.py


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'description', 'price', 'size']

# class ProductForm(forms.Form):
#     class Meta:
#         model = Product

#         code = forms.CharField(max_length=20)
#         name = forms.CharField(max_length=50)
#         description = forms.Textarea()
#         price = forms.IntegerField()
#         size = forms.CharField()
