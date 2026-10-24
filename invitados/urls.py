from django.urls import path

from . import views

app_name = 'invitados'

urlpatterns = [
    path('nuevo/', views.crear_invitado, name='crear'),
]
