from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
from .models import Plant, Order
import json


# ------------------ HOME ------------------
def home(request):
    plants = Plant.objects.all()
    return render(request, 'home.html', {'plants': plants})


# ------------------ DASHBOARD ------------------
@login_required
def dashboard(request):
    if not request.user.is_staff:
        return redirect('home')

    orders_all = Order.objects.select_related('plant', 'user')
    total_orders = orders_all.count()
    total_revenue = sum(o.quantity * o.plant.price for o in orders_all)

    plant_summary = (
        Order.objects.values('plant__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
    )

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

    paginator = Paginator(orders_with_subtotal, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'plant_summary': plant_summary,
        'page_obj': page_obj,
    })


# ------------------ ADD ------------------
def add_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        Plant.objects.create(name=name, price=price, stock=stock, image=image)
        return redirect('home')
    return render(request, 'add_plant.html')


# ------------------ BUY ------------------
@login_required
def buy_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if plant.stock >= quantity:
            plant.stock -= quantity
            plant.save()
            Order.objects.create(user=request.user, plant=plant, quantity=quantity)
    return redirect('home')


# ------------------ BUY CART ------------------
@login_required
def buy_cart(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data', '[]')
        try:
            cart = json.loads(cart_data)
        except:
            return redirect('home')

        for item in cart:
            plant_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            plant = get_object_or_404(Plant, id=plant_id)
            if plant.stock >= quantity:
                plant.stock -= quantity
                plant.save()
                Order.objects.create(user=request.user, plant=plant, quantity=quantity)

    return redirect('home')


# ------------------ EDIT ------------------
def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        plant.price = request.POST.get('price')
        plant.stock = request.POST.get('stock')
        plant.save()
        return redirect('home')
    return render(request, 'edit_plant.html', {'plant': plant})


# ------------------ DELETE ------------------
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('home')
