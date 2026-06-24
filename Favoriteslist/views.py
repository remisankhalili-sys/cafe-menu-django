from django.shortcuts import render, redirect

from .models import Product

def product_view(request):
    products = Product.objects.all()
    return render(request, 'Favoriteslist/products_list.html', {'products': products} )
        