from django import forms

from .models import Evento

FORMATO_FECHA = '%Y-%m-%dT%H:%M'


class EventoForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label='Fecha y hora',
        input_formats=[FORMATO_FECHA],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}, format=FORMATO_FECHA
        ),
    )

    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha', 'lugar']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 4})}
