from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                              # ← เพิ่มใหม่
    path('dashboard/', views.dashboard, name='dashboard'),          # ← เพิ่มใหม่
    path('add/', views.add_plant, name='add_plant'),
    path('buy/<int:plant_id>/', views.buy_plant, name='buy_plant'),
    path('edit/<int:plant_id>/', views.edit_plant, name='edit_plant'),
    path('delete/<int:plant_id>/', views.delete_plant, name='delete_plant'),
    path('buy-cart/', views.buy_cart, name='buy_cart'),
]