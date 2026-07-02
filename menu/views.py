from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, MenuItem, Wishlist, Order, OrderItem, Comment, Ingredient
from .cart import Cart


def menu_home(request):
    """Display all menu items with optional category filtering."""
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

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(customer=request.user).values_list('menu_item_id', flat=True)
        )

    return render(request, 'menu/menu_home.html', {
        'categories': categories,
        'items': items,
        'selected_category': selected_category,
        'wishlist_ids': wishlist_ids,
    })


def menu_item_detail(request, pk):
    """Display details, ingredients, and comments for a single menu item."""
    item = get_object_or_404(MenuItem.objects.prefetch_related('images', 'ingredients', 'comments'), pk=pk)
    primary_image = item.images.filter(is_primary=True).first()
    other_images = item.images.filter(is_primary=False)
    ingredients = item.ingredients.all()
    comments = item.comments.select_related('customer').order_by('-created_at')

    user_comment = None
    if request.user.is_authenticated:
        user_comment = comments.filter(customer=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text', '').strip()
        if text:
            Comment.objects.update_or_create(
                customer=request.user,
                menu_item=item,
                defaults={'text': text}
            )
            messages.success(request, 'Your comment has been saved.')
            return redirect('menu:menu_item_detail', pk=pk)

    return render(request, 'menu/menu_item_detail.html', {
        'item': item,
        'primary_image': primary_image,
        'other_images': other_images,
        'ingredients': ingredients,
        'comments': comments,
        'user_comment': user_comment,
    })


def cart_detail(request):
    """Display the current cart."""
    cart = Cart(request)
    return render(request, 'menu/cart.html', {'cart': cart})


@require_POST
def cart_add(request, pk):
    """Add a menu item to the cart."""
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item_id=item.id, quantity=quantity)
    return redirect('menu:cart_detail')


@require_POST
def cart_remove(request, pk):
    """Remove a menu item from the cart."""
    cart = Cart(request)
    cart.remove(item_id=pk)
    return redirect('menu:cart_detail')


@require_POST
def cart_update(request, pk):
    """Update the quantity of a menu item in the cart."""
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.update(item_id=pk, quantity=quantity)
    return redirect('menu:cart_detail')


@login_required
def wishlist(request):
    """Display the customer's wishlist."""
    wishlist_items = Wishlist.objects.filter(customer=request.user).select_related('menu_item')
    for entry in wishlist_items:
        entry.menu_item.primary_image = (
            entry.menu_item.images.filter(is_primary=True).first()
            or entry.menu_item.images.first()
        )
    return render(request, 'menu/wishlist.html', {'items': wishlist_items})

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


@login_required
def checkout(request):
    """Convert cart items into an Order and clear the cart."""
    cart = Cart(request)
    items = cart.get_items()

    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu:cart_detail')

    order = Order.objects.create(customer=request.user)
    for entry in items:
        OrderItem.objects.create(
            order=order,
            menu_item=entry['item'],
            quantity=entry['quantity'],
            price=entry['item'].price
        )
    cart.clear()
    messages.success(request, f'Order #{order.pk} placed successfully!')
    return redirect('menu:menu_home')

