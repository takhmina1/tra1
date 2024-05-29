# ваш_проект/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),  # Замените 'tours' на имя вашего приложения
]
