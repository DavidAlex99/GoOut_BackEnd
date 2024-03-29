from django import forms
from .models import ImagenEvento, Evento, Comida, Contacto, ImagenContacto, SobreNos, ImagenSobreNos , Emprendedor, Emprendimiento
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Emprendedor
from django.forms import inlineformset_factory


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

# registro de emprendimiento
class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ['nombre', 'descripcion', 'categoria', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'categoria', 'disponibles', 'precio']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ImagenEventoForm(forms.ModelForm):
    class Meta:
        model = ImagenEvento
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

ImagenEventoFormSet = inlineformset_factory(
    Evento, ImagenEvento, 
    form=ImagenEventoForm, 
    extra=4,  # Puedes ajustar el número de formularios extra que quieres mostrar.
    can_delete=True,  # Permite marcar imágenes para eliminar.
)

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'categoria', 'emprendimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'emprendimiento': forms.HiddenInput(),  # Asumiendo que se establece automáticamente en la vista o está oculto para el usuario.
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['descripcion', 'direccion', 'direccion_secundaria', 'correo', 'telefono', 'latitud', 'longitud']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_secundaria': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            # campos que se va usar para la api de google maps
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }

class ImagenContactoForm(forms.ModelForm):
    class Meta:
        model = ImagenContacto
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

ImagenContactoFormSet = inlineformset_factory(
    Contacto, ImagenContacto, 
    form=ImagenContactoForm, 
    extra=4,  # Cambiado de 4 a 0 para no mostrar formularios extras por defecto.
    can_delete=True,  # Permite marcar imágenes para eliminar.
)

    
class SobreNosForm(forms.ModelForm):
    class Meta:
        model = SobreNos
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ImagenSobreNosForm(forms.ModelForm):
    class Meta:
        model = ImagenSobreNos
        fields = ['imagen']
        widgets = {
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

ImagenSobreNosFormSet = inlineformset_factory(
    SobreNos, ImagenSobreNos, 
    form=ImagenSobreNosForm, 
    extra=4,  # Puedes ajustar el número de formularios extra que quieres mostrar.
    can_delete=True,  # Permite marcar imágenes para eliminar.
)