from django.shortcuts import render, get_object_or_404
from .models import Category, MenuItem


def menu_home(request):
    categories = Category.objects.prefetch_related('items__images').all()
    selected_category = request.GET.get('category')

    if selected_category:
        items = MenuItem.objects.prefetch_related('images').filter(
            category__name__iexact=selected_category,
            is_available=True
        )
    else:
        items = MenuItem.objects.prefetch_related('images').filter(is_available=True)

    return render(request, 'menu/menu_home.html', {
        'categories': categories,
        'items': items,
        'selected_category': selected_category,
    })


def menu_item_detail(request, pk):
    item = get_object_or_404(MenuItem.objects.prefetch_related('images'), pk=pk)
    primary_image = item.images.filter(is_primary=True).first()
    other_images = item.images.filter(is_primary=False)
    return render(request, 'menu/menu_item_detail.html', {
        'item': item,
        'primary_image': primary_image,
        'other_images': other_images,
    })