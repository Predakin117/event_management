from django import forms
from django.core.validators import RegexValidator


class FormularioCedula(forms.Form):
    cedula = forms.CharField(
        label='Número de cédula',
        max_length=12,
        validators=[
            RegexValidator(
                r'^\d{5,12}$',
                'Escribe solo números (entre 5 y 12 dígitos), sin puntos ni espacios.',
            )
        ],
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 1020304050',
            'inputmode': 'numeric',
            'autofocus': True,
        }),
    )
