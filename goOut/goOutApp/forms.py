from django import forms
from .models import Evento, Alimento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'imagen']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nombre', 'precio', 'descripcion', 'imagen']

