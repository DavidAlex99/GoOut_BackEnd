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
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class UbicacionForm(forms.ModelForm):
    class Meta:
        model: Ubicacion
        fields = ['direccion', 'direccion_secundaria', 'imagen']

class ContactoForm(forms.ModelForm):
    class Meta:
        model: Contacto
        fields = ['emprendedor', 'correo', 'telefono', 'imagen']

class SobreNosForm(forms.ModelForm):
    class Meta:
        model: SobreNos
        fields = ['descripcion', 'imagen']
