from django.shortcuts import render

from . import servicios
from .forms import FormularioCedula


def confirmar(request):
    contexto = {'buscado': False, 'invitaciones': [], 'nombre': None}

    if 'cedula' in request.GET:
        formulario = FormularioCedula(request.GET)
        if formulario.is_valid():
            invitaciones = servicios.buscar_invitaciones(
                formulario.cleaned_data['cedula']
            )
            contexto.update(
                buscado=True,
                invitaciones=invitaciones,
                nombre=invitaciones[0].nombre if invitaciones else None,
            )
    else:
        formulario = FormularioCedula()

    contexto['formulario'] = formulario
    return render(request, 'confirmacion/confirmar.html', contexto)
