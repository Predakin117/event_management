from django.shortcuts import get_object_or_404, render

from .models import Evento


def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista.html', {'eventos': eventos})


def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'eventos/detalle.html', {'evento': evento})
