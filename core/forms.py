# Contenido de core/forms.py
from django import forms
from .models import MensajeContacto

class ContactoForm(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre Completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}),
            'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del Mensaje'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'asunto': 'Asunto',
            'mensaje': 'Tu Mensaje',
        }
        help_texts = {
            'email': 'Nunca compartiremos tu correo electrónico con nadie más.',
        }
        error_messages = {
            'nombre': {
                'required': "Por favor, introduce tu nombre.",
            },
            'email': {
                'required': "Por favor, introduce tu correo electrónico.",
                'invalid': "Por favor, introduce una dirección de correo electrónico válida."
            },
            'asunto': {
                'required': "Por favor, introduce un asunto.",
            },
            'mensaje': {
                'required': "Por favor, escribe tu mensaje.",
            },
        }
