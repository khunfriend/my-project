from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('shop/', include('shop.urls')),  # 👈 ต้องมี
    path('admin/', admin.site.urls),
]