from django import forms
from .models import Evento, Alimento, Categoria, Contacto, Ubicacion, SobreNos

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'imagen']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Alimento
        fields = ['nombre', 'precio', 'descripcion', 'categoria', 'imagen']

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class UbicacionForm(forms.ModelForm):
    class Meta:
        model: Ubicacion
        fields = ['imagen', 'titulo', 'descripcion']

class ContactoForm(forms.ModelForm):
    class Meta:
        model: Contacto
        fields = ['imagen', 'correo', 'telefono']

class SobreNosForm(forms.ModelForm):
    class Meta:
        model: SobreNos
        fields = ['descripcion', 'imagen']
