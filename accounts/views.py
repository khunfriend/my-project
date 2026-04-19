from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username นี้มีคนใช้แล้ว'})

        user = User.objects.create_user(username=username, password=password)
        group, _ = Group.objects.get_or_create(name='customer')
        user.groups.add(group)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard') if user.is_staff else redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username หรือ Password ผิด'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')