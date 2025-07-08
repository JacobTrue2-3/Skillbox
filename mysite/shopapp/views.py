from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User

from .models import Product
from .models import Order

def shop_index(request):
    products = [
        ('Laptop', 1999),
        ('Desktop', 2999),
        ('Smartphone', 999),
    ]
    context = {
        'products': products,
    }
    return render(request, 'shopapp/shop-index.html', context=context)

def groups_list(request):
    context = {
        'groups': Group.objects.prefetch_related('permissions').all(),
    }
    return render(request, 'shopapp/groups-list.html', context=context)

def products_list(request):
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'shopapp/products-list.html', context=context)

def orders_list(request):
    context = {
        'orders': Order.objects.select_related('user').prefetch_related("products").all(),

    }
    return render(request, 'shopapp/orders-list.html', context=context)