from django.core.validators import RegexValidator
from django.db import models

from eventos.models import Evento


class Invitado(models.Model):
    nombre = models.CharField(max_length=150)
    cedula = models.CharField(
        'cédula',
        max_length=12,
        validators=[
            RegexValidator(
                r'^\d{5,12}$',
                'Escribe solo números (entre 5 y 12 dígitos), sin puntos ni espacios.',
            )
        ],
        help_text='Solo números, sin puntos ni espacios.',
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='invitados',
    )

    class Meta:
        ordering = ['evento__fecha', 'nombre']
        constraints = [
            models.UniqueConstraint(
                fields=['evento', 'cedula'],
                name='invitado_unico_por_evento',
                violation_error_message='Esa cédula ya está invitada a este evento.',
            )
        ]

    def __str__(self):
        return f'{self.nombre} ({self.cedula}) → {self.evento}'
