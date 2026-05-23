from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Маршрути авторизації
    path('', include('portal.urls')),  # Маршрути нашого додатка
]