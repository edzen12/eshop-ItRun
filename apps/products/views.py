from django.shortcuts import render
from apps.products.models import Product, Category

def home(request):
    products = Product.objects.all()
    sliders = Product.objects.all()[:2]
    categories = Category.objects.all()[:8]
    context = {
        'products':products,
        'sliders':sliders,
        'categories':categories,
    }
    return render(request, 'index.html', context)