from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from apps.products.forms import SearchForm
from apps.products.models import Product, Category, Images


def search_view(request):
    form = SearchForm()
    query = ''
    products = []
    categories = [] 
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            products = Product.objects.filter(
                (Q(title__icontains=query) | Q(keywords__icontains=query)),
                status='True'
            )

            categories = Category.objects.filter(
                (Q(title__icontains=query) | Q(keywords__icontains=query)),
                status='True'
            )
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


def contact(request):
    categories = Category.objects.all()[:6]
    return render(request, 'pages/contact.html', {'categories':categories})