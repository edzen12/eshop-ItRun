from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout, get_user_model
from django.contrib.auth.decorators import login_required
from apps.products.models import Category
User = get_user_model()


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


def reg_view(request):
    categories = Category.objects.all()[:6]
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            return render(request, 'auth/register.html', {'error':'Пароли не совпадают', 'categories':categories})
        if len(password)< 6:
            return render(request, 'auth/register.html', {'error':'Пароль должен быть больше 6 символов', 'categories':categories})
        if password == password2:
            User.objects.create_user(username=login, password=password)
            usr = authenticate(request, username=login, password=password)
            if usr is not None: # проверка на сущ
                user_login(request, usr)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'auth/register.html', {'error':'Неверный логин или пароль', 'categories':categories})
    return render(request, 'auth/register.html', {'categories':categories})


def logout_view(request):
    user_logout(request)
    return HttpResponseRedirect('/')


@login_required
def profile_view(request):
    categories = Category.objects.all()[:6]
    return render(request, 'auth/profile.html', {'categories':categories})