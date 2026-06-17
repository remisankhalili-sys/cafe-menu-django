from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem


def menu_home(request):
    categories = Category.objects.prefetch_related(
        'items__images'
    ).all()
    return render(request, 'menu/menu_home.html', {'categories': categories})


def menu_item_detail(request, pk):
    item = get_object_or_404(MenuItem.objects.prefetch_related('images'), pk=pk)
    primary_image = item.images.filter(is_primary=True).first()
    other_images = item.images.filter(is_primary=False)
    return render(request, 'menu/menu_item_detail.html', {
        'item': item,
        'primary_image': primary_image,
        'other_images': other_images,
    })
