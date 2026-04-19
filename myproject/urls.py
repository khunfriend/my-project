from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('shop.urls')),          # ← เปลี่ยนจาก accounts เป็น shop
    path('accounts/', include('accounts.urls')),  # ← accounts ดูแค่ login/logout/register
    path('admin/', admin.site.urls),
]