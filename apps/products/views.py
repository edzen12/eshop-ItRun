from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from apps.products.forms import SearchForm
from apps.products.models import Product, Category, Images, Faq
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
        'form':form, 
        'query':query,
        'products':products,
        'categories':categories,
    }
    return render(request, 'pages/search_results.html', context)


def home(request):
    products = Product.objects.all()
    sliders = Product.objects.all()[:2]
    categories = Category.objects.all()[:6]
    context = {
        'products':products,
        'sliders':sliders,
        'categories':categories,
    }
    return render(request, 'index.html', context)


def product_detail(request, slug):
    categories = Category.objects.all()[:6]
    product = Product.objects.get(slug=slug)
    images = Images.objects.filter(product=product)
    context = {
        'categories':categories,
        'product':product,
        'images':images,
    }
    return render(request, 'pages/product-detail.html', context)


def category_detail(request, slug):
    categories = Category.objects.all()[:6]
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='True')
    context = {
        'categories':categories,
        'products':products,
        'category':category,
    }
    return render(request, 'pages/category-detail.html', context)


def male_products(request):
    products = Product.objects.filter(gender="male", status='True')
    categories = Category.objects.all()[:6]
    context = {
        'products':products,
        'categories':categories,
        'gender_title': 'Мужские товары',
    }
    return render(request, 'pages/gender_products.html', context)


def female_products(request):
    products = Product.objects.filter(gender="female", status='True')
    categories = Category.objects.all()[:6]
    context = {
        'products':products,
        'categories':categories,
        'gender_title': 'Женские товары',
    }
    return render(request, 'pages/gender_products.html', context)


def faq(request):
    faqs = Faq.objects.all()
    categories = Category.objects.all()[:6]
    context = {
        'faqs':faqs,
        'categories':categories,
        'title_faq': 'Вопросы / Ответы',
    }
    return render(request, 'pages/faq.html', context)


def contact(request):
    categories = Category.objects.all()[:6]
    return render(request, 'pages/contact.html', {'categories':categories})



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
        'categories':categories,
        'cart':cart,
    }
    return render(request, 'pages/cart.html', context)