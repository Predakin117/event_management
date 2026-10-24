from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import InvitadoForm


@login_required
def crear_invitado(request):
    if request.method == 'POST':
        formulario = InvitadoForm(request.POST)
        if formulario.is_valid():
            invitado = formulario.save()
            return redirect('eventos:detalle', pk=invitado.evento_id)
    else:
        # Permite llegar desde el detalle de un evento con el evento preseleccionado.
        formulario = InvitadoForm(initial={'evento': request.GET.get('evento')})
    return render(request, 'invitados/formulario.html', {'formulario': formulario})
