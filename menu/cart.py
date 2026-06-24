from .models import MenuItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, item_id, quantity=1):
        item_id = str(item_id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0}
        self.cart[item_id]['quantity'] += quantity
        self.save()

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update(self, item_id, quantity):
        item_id = str(item_id)
        if quantity <= 0:
            self.remove(item_id)
        else:
            self.cart[item_id] = {'quantity': quantity}
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.prefetch_related('images').filter(id__in=item_ids)
        result = []
        for item in items:
            result.append({
                'item': item,
                'quantity': self.cart[str(item.id)]['quantity'],
                'total_price': item.price * self.cart[str(item.id)]['quantity'],
            })
        return result

    def get_total(self):
        items = self.get_items()
        return sum(i['total_price'] for i in items)

    def get_count(self):
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        self.session['cart'] = {}
        self.save()