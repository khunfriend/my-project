from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from shop.models import Plant, Order
from django.db.models import Sum
from django.core.paginator import Paginator


@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    orders_all = Order.objects.select_related('plant', 'user')

    # ✅ ยอดรวม
    total_orders = orders_all.count()
    total_revenue = sum(o.quantity * o.plant.price for o in orders_all)

    # ✅ จำนวนต้นไม้แต่ละประเภท
    plant_summary = (
        Order.objects.values('plant__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
    )

    # ✅ คำนวณ subtotal ใน Python
    all_orders = Order.objects.select_related('plant', 'user').order_by('-created_at')
    orders_with_subtotal = []
    for o in all_orders:
        orders_with_subtotal.append({
            'username': o.user.username,
            'plant_name': o.plant.name,
            'quantity': o.quantity,
            'subtotal': o.quantity * o.plant.price,
            'created_at': o.created_at,
        })

    # ✅ Pagination 10 ต่อหน้า
    paginator = Paginator(orders_with_subtotal, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'plant_summary': plant_summary,
        'page_obj': page_obj,
    })


def home(request):
    plants = Plant.objects.all()
    return render(request, 'home.html', {'plants': plants})


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