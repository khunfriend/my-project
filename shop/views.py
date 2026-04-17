from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Plant, Order
import json


def add_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        Plant.objects.create(name=name, price=price, stock=stock)
        return redirect('home')
    return render(request, 'add_plant.html')


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


def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if request.method == 'POST':
        # plant.name = request.POST.get('name')
        plant.price = request.POST.get('price')
        plant.stock = request.POST.get('stock')
        plant.save()
        return redirect('home')
    return render(request, 'edit_plant.html', {'plant': plant})


def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('home')