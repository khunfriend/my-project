from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from shop.models import Plant
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from shop.models import Order

@staff_member_required
def dashboard(request):
    orders = Order.objects.all()
    return render(request, 'dashboard.html', {'orders': orders})

# ------------------ HOME ------------------
def home(request):
    plants = Plant.objects.all()
    return render(request, 'home.html', {'plants': plants})


# ------------------ REGISTER ------------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Username นี้มีคนใช้แล้ว'
            })

        user = User.objects.create_user(username=username, password=password)

        group, _ = Group.objects.get_or_create(name='customer')
        user.groups.add(group)

        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


# ------------------ LOGIN ------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_staff:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Username หรือ Password ผิด'
            })

    return render(request, 'login.html')


# ------------------ DASHBOARD ------------------
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    return render(request, 'dashboard.html')


# ------------------ LOGOUT ------------------
def logout_view(request):
    logout(request)
    return redirect('home')