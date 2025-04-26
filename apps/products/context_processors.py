# apps/products/context_processors.py

def cart_context(request):
    cart = request.session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

    return {
        'cart_items': cart,
        'cart_total_quantity': total_quantity,
        'cart_total_price': total_price,
    }