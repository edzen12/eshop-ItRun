from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from apps.products.forms import SearchForm
from apps.products.models import Product, Category, Images, Faq, VideoBlog
from apps.products.cart import Cart


def search_view(request):
    form = SearchForm()
    query = ''
    products = []
    categories = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query'].strip()
            words = query.split()
            product_query = Q()
            category_query = Q()

            for word in words:
                product_query |= Q(title__icontains=word) | Q(keywords__icontains=word)
                category_query |= Q(title__icontains=word) | Q(keywords__icontains=word)

            products = Product.objects.filter(product_query, status='True')
            categories = Category.objects.filter(category_query, status='True')

    context = {
        'form': form,
        'query': query,
        'products': products,
        'categories': categories,
    }
    return render(request, 'pages/search_results.html', context)


def home(request):
    products = Product.objects.all()
    sliders = Product.objects.filter(
        Q(discount_percent__isnull=False) | Q(discount_price__isnull=False),
        status='True'
    )[:5]
    categories = Category.objects.all()[:6]
    context = {
        'products': products,
        'sliders': sliders,
        'categories': categories,
    }
    return render(request, 'index.html', context)


def product_detail(request, slug):
    categories = Category.objects.all()[:6]
    product = get_object_or_404(Product, slug=slug)
    images = Images.objects.filter(product=product)
    context = {
        'categories': categories,
        'product': product,
        'images': images,
    }
    return render(request, 'pages/product-detail.html', context)


def category_detail(request, slug):
    categories = Category.objects.all()[:6]
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='True')
    context = {
        'categories': categories,
        'products': products,
        'category': category,
    }
    return render(request, 'pages/category-detail.html', context)


def male_products(request):
    products = Product.objects.filter(gender="male", status='True')
    categories = Category.objects.all()[:6]
    context = {
        'products': products,
        'categories': categories,
        'gender_title': 'Мужские товары',
    }
    return render(request, 'pages/gender_products.html', context)


def female_products(request):
    products = Product.objects.filter(gender="female", status='True')
    categories = Category.objects.all()[:6]
    context = {
        'products': products,
        'categories': categories,
        'gender_title': 'Женские товары',
    }
    return render(request, 'pages/gender_products.html', context)


def faq(request):
    faqs = Faq.objects.all()
    categories = Category.objects.all()[:6]
    context = {
        'faqs': faqs,
        'categories': categories,
        'title_faq': 'Вопросы / Ответы',
    }
    return render(request, 'pages/faq.html', context)


def vlog(request): 
    vlogs = VideoBlog.objects.all()
    categories = Category.objects.all()[:6]
    context = { 
        'vlogs': vlogs,
        'categories': categories,
        'title_vlog': 'Влог',
    }
    return render(request, 'pages/vlog.html', context)


def discount_products(request):
    categories = Category.objects.all()[:6]
    products = Product.objects.filter(status="True").filter(
        Q(discount_price__isnull=False) | Q(discount_percent__isnull=False)
    )
    context = { 
        'categories': categories,
        'products': products,
        'title_dis': 'Товары со скидкой',
    }
    return render(request, 'pages/discount_products.html', context)


def newsletter(request):
    categories = Category.objects.all()[:6]
    return render(request, 'pages/newsletter.html', {'categories': categories})


def contact(request):
    categories = Category.objects.all()[:6]
    return render(request, 'pages/contact.html', {'categories': categories})


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()[:6]
    context = {
        'cart_items': cart,
        'categories': categories,
        'cart_total_quantity': sum(item['quantity'] for item in cart),
        'cart_total_price': sum(float(item['price']) * item['quantity'] for item in cart),
    }
    return render(request, 'pages/cart.html', context)


def checkout_view(request):
    categories = Category.objects.all()[:6]
    cart = Cart(request)
    context = {
        'categories': categories,
        'cart': cart,
        'cart_total_price': cart.get_total_price(),
    }
    return render(request, 'pages/checkout.html', context)


@csrf_exempt
def cart_add_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
        except (json.JSONDecodeError, ValueError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {
                'price': str(product.price),
                'quantity': quantity,
                'title': product.title,
                'image': product.image.url if product.image else '',
            }

        request.session['cart'] = cart

        total_quantity = sum(item['quantity'] for item in cart.values())
        total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

        return JsonResponse({
            'success': True,
            'cart_total_quantity': total_quantity,
            'cart_total_price': round(total_price, 2),
            'cart_currency': 'сом',
        })
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def cart_remove_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({'success': False, 'error': 'Invalid JSON data.'}, status=400)

        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart

            total_quantity = sum(item['quantity'] for item in cart.values())
            total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())

            return JsonResponse({
                'success': True,
                'cart_total_quantity': total_quantity,
                'cart_total_price': round(total_price, 2),
                'cart_currency': 'сом',
            })

        return JsonResponse({'success': False, 'error': 'Product not found in cart.'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)