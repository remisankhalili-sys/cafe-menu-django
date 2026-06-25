from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Category, MenuItem, Wishlist
from .cart import Cart


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

    for item in items:
        item.primary_image = item.images.filter(is_primary=True).first() or item.images.first()

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


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'menu/cart.html', {'cart': cart})


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item_id=item.id, quantity=quantity)
    return redirect('menu:cart_detail')


@require_POST
def cart_remove(request, pk):
    cart = Cart(request)
    cart.remove(item_id=pk)
    return redirect('menu:cart_detail')


@require_POST
def cart_update(request, pk):
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(item_id=pk, quantity=quantity)
    return redirect('menu:cart_detail')

@login_required
def wishlist(request):
    """Display the customer's wishlist."""
    items = Wishlist.objects.filter(customer=request.user).select_related('menu_item')
    return render(request, 'menu/wishlist.html', {'items': items})


@login_required
def wishlist_toggle(request, pk):
    """Add or remove a menu item from the customer's wishlist."""
    item = get_object_or_404(MenuItem, pk=pk)
    wishlist_item, created = Wishlist.objects.get_or_create(
        customer=request.user,
        menu_item=item
    )
    if not created:
        wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'menu:menu_home'))