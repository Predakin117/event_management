from django.urls import path

from . import views

app_name = 'eventos'

urlpatterns = [
    path('', views.lista_eventos, name='lista'),
    path('eventos/<int:pk>/', views.detalle_evento, name='detalle'),
]
