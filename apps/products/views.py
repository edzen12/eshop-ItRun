from django.shortcuts import render
from apps.products.models import Product, Category, Images

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
    images = Images.objects.all()
    context = {
        'categories':categories,
        'product':product,
        'images':images,
    }
    return render(request, 'product-detail.html', context)
