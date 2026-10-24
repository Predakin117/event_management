"""Capa de lógica de negocio de la app `confirmacion`.

La vista solo recibe el formulario y devuelve HTML; la consulta de
invitaciones vive aquí.
"""
from invitados.models import Invitado


def buscar_invitaciones(cedula):
    """Devuelve las invitaciones (con su evento) de la persona con esa cédula.

    Si la cédula no existe, devuelve una lista vacía.
    """
    return list(
        Invitado.objects
        .filter(cedula=cedula.strip())
        .select_related('evento')
        .order_by('evento__fecha')
    )
