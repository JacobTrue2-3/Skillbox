from django import forms
from django.forms import ModelForm
from .models import Product
from django.contrib.auth.models import Group

# from django.core import validators

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000)
#     description = forms.CharField(
#         label='Product description',
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 20}),
#         validators=[validators.RegexValidator(
#             regex='Product',
#             message='Product name should start with "Product"',
#         )]
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'discount']
        

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name']