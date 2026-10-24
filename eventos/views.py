from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventoForm
from .models import Evento


def lista_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/lista.html', {'eventos': eventos})


def detalle_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    # La lista de invitados solo se muestra a usuarios con sesión iniciada.
    invitados = evento.invitados.all() if request.user.is_authenticated else None
    return render(
        request,
        'eventos/detalle.html',
        {'evento': evento, 'invitados': invitados},
    )


@login_required
def crear_evento(request):
    if request.method == 'POST':
        formulario = EventoForm(request.POST)
        if formulario.is_valid():
            evento = formulario.save()
            return redirect('eventos:detalle', pk=evento.pk)
    else:
        formulario = EventoForm()
    return render(request, 'eventos/formulario.html', {'formulario': formulario})
