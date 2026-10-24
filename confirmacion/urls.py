from django.urls import path

from . import views

app_name = 'confirmacion'

urlpatterns = [
    path('', views.confirmar, name='confirmar'),
]
