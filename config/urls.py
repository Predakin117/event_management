"""Enrutador principal del proyecto.

Cada app define sus propias URLs; aquí solo se conectan.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cuenta/', include('django.contrib.auth.urls')),  # login, logout...
    path('invitados/', include('invitados.urls')),
    path('confirmacion/', include('confirmacion.urls')),
    path('', include('eventos.urls')),
]
