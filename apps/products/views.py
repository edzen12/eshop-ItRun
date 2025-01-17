from django.shortcuts import render
from apps.products.models import Product

def home(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'index.html', context)