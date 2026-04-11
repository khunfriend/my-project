from django.shortcuts import render, redirect, get_object_or_404
from .models import Plant
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'orders': orders})
# ---------------- ADD ----------------
def add_plant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')

        Plant.objects.create(name=name, price=price, stock=stock)
        return redirect('home')

    return render(request, 'add_plant.html')


# ---------------- BUY ----------------
def buy_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if plant.stock > 0:
        plant.stock -= 1
        plant.save()

    return redirect('home')


# ---------------- EDIT ----------------
def edit_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'POST':
        plant.name = request.POST.get('name')
        plant.price = request.POST.get('price')
        plant.stock = request.POST.get('stock')
        plant.save()
        return redirect('home')

    return render(request, 'edit_plant.html', {'plant': plant})


# ---------------- DELETE ----------------
def delete_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    plant.delete()
    return redirect('home')
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Plant, Order


@login_required
def buy_plant(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)

    if plant.stock > 0:
        # ลด stock
        plant.stock -= 1
        plant.save()

        # ✅ บันทึก order
        Order.objects.create(
            user=request.user,
            plant=plant,
            quantity=1
        )

    return redirect('home')