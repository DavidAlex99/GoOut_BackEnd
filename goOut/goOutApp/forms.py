from django import forms
from .models import Evento, Alimento, Categoria, Contacto, Ubicacion, SobreNos, Emprendedor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Emprendedor

# formulario personalizado para el inicio de sesion
class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

# formulario para muestreo para actualizar informacion como 
# nobre, edad desues de registrar
class EmprendedorRegisterForm(UserCreationForm):
    # definicion de los campos del emprendedor
    nombre = forms.CharField(
        label='Ingrese su nombre',  # Texto que se mostrará para el campo nombre
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    edad = forms.IntegerField(
        label='Ingrese su edad',  # Texto que se mostrará para el campo edad
        required=True, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('edad', 'nombre',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            Emprendedor.objects.create(user=user, edad=self.cleaned_data['edad'], nombre=self.cleaned_data['nombre'])
        return user

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

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
# constructor que hace que se pase como argumento adicional un emprendedor el cual se usara para filtrara
# por las categorias que son propias del emprendedor
    def __init__(self, *args, **kwargs):
        emprendedor = kwargs.pop('emprendedor', None)
        super(ComidaForm, self).__init__(*args, **kwargs)
        if emprendedor:
            self.fields['categoria'].queryset = Categoria.objects.filter(emprendedor=emprendedor)

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
        model = Contacto
        fields = ['emprendedor', 'correo', 'telefono', 'imagen']
        widgets = {
            'emprendedor': forms.Select(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class SobreNosForm(forms.ModelForm):
    class Meta:
        model = SobreNos
        fields = ['descrpcion', 'imagen']
        widgets = {
            'descrpcion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),
        }