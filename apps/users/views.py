from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, get_user_model
from django.contrib.auth.decorators import login_required
from apps.products.models import Category


def login_view(request):
    categories = Category.objects.all()[:6]
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        usr = authenticate(request, username=login, password=password)
        if usr is not None: # проверка на сущ
            user_login(request, usr)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'auth/login.html', {'error':'Неверный логин или пароль', 'categories':categories})
    return render(request, 'auth/login.html', {'categories':categories})