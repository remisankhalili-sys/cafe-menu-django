from django.shortcuts import render
from .models import Category

def menu_home(request):
    categories = Category.objects.all()
    return render(request, 'menu/menu_home.html', {'categories': categories})
