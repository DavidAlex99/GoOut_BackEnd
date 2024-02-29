from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ComidaForm, CategoriaComidaForm, SobreNosForm, UbicacionForm, ContactoForm, EmprendedorRegisterForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, Comida, CategoriaComida, Emprendedor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseNotAllowed
import os

# La vista personalizada para el inicio de sesión
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm  # Asegúrate de tener un CustomLoginForm o puedes usar el predeterminado
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('user_profile', kwargs={'username': self.request.user.username})

# La vista del perfil de usuario
@login_required
def user_profile(request, username):
    # Asegúrate de que el nombre de usuario en la URL coincida con el usuario logueado
    if username != request.user.username:
        return redirect('user_profile', username=request.user.username)
    return render(request, 'user_profile.html', {'username': username})

# La vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = EmprendedorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_profile', username=user.username)
    else:
        form = EmprendedorRegisterForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return render(request, "home.html")

def menu(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
     # aqui se renderizaran los eventos de la base de datos de acuerdo al emprendedor
    emprendedor = request.user.emprendedor
    categoriasComida = CategoriaComida.objects.filter(emprendedor=emprendedor)
    comidas = Comida.objects.filter(emprendedor=emprendedor)
    context = {
        # los elementos de la bbdd que se van a renderizar
        "categoriasComida": categoriasComida,
        "comidas": comidas,
        "username": username,
    }
    return render(request, "menu.html", context)

def subirComida(request, username):
    # se pasa el emprendedor que esta logueado actualmente
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    emprendedor = request.user.emprendedor
    if request.method == "POST":
        # se pasa como argumento adicional el emprendedor actual al forms
        formulario_servicio = ComidaForm(request.POST, request.FILES, emprendedor=emprendedor) 
        if formulario_servicio.is_valid():
            comida = formulario_servicio.save(commit=False) # Guarda el formulario pero no el objeto
            comida.emprendedor = emprendedor  # Asigna el usuario logueado al objeto comida
            comida.save()
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        # Pasar el emprendedor al inicializar el formulario para filtrar las categorías
        formulario_servicio = ComidaForm(emprendedor=emprendedor)
    return render(request, "subirComida.html", {'miFormularioComida': formulario_servicio})

def acerca(request, username):
# Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = SobreNosForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = SobreNosForm()
    return render(request, "acerca.html", {'miFormularioSobreNos': formulario_servicio})

#vista para el contacto
def contacto(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = ContactoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ContactoForm()
    return render(request, "contacto.html", {'miFormularioContacto': formulario_servicio})


#vista para la ubicacion
def ubicacion(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = UbicacionForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = UbicacionForm()
    return render(request, "ubicacion.html", {'miFormularioUbicacion': formulario_servicio})

# vista para la galeria
def galeria(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    # aqui se renderizaran los eventos de la base de datos de acuerdoal emprendedor
    emprendedor = request.user.emprendedor
    eventos = Evento.objects.filter(emprendedor=emprendedor)
    return render(request, "galeria.html", {"eventos": eventos})

# para los formularios para subir imagen 
def subirEvento(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = EventoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            evento = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            evento.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            evento.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Evento', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = EventoForm()
    return render(request, "subirEvento.html", {'miFormularioImagen': formulario_servicio})




def subirCategoriaComida(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = CategoriaComidaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            categoriaComida = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            categoriaComida.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            categoriaComida.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = CategoriaComidaForm()
    return render(request, "subirCategoriaComida.html", {'miFormularioCategoriaComida': formulario_servicio})

@login_required
def eliminarCategoriaComida(request, username, categoriaComida_id):
    # Solo permitir esta acción si el método es POST y el usuario está autenticado
    if request.method == "POST" and request.user.username == username:
        categoria = get_object_or_404(CategoriaComida, id=categoriaComida_id, emprendedor=request.user.emprendedor)
        
         # Eliminar las imágenes de los alimentos asociados a la categoría
        comidas = Comida.objects.filter(categoriaComida=categoria)
        for comida in comidas:
            if comida.imagen and os.path.isfile(comida.imagen.path):
                os.remove(comida.imagen.path)
            comida.delete()  # Eliminar la instancia de Comida

        # Eliminar la imagen de la categoría
        if categoria.imagen and os.path.isfile(categoria.imagen.path):
            os.remove(categoria.imagen.path)
        
        categoria.delete()  # Eliminar la instancia de CategoriaComida
        messages.success(request, "Categoría y alimentos asociados eliminados correctamente.")
        return redirect('Menu', username=username)

    else:
        messages.error(request, "No se puede eliminar la categoría.")
        return redirect('Menu', username=username)

@login_required
def eliminarComida(request, username, comida_id):

    # Asegúrate de que el método es POST y que el usuario está autenticado
    if request.method == "POST" and request.user.username == username:
        comida = get_object_or_404(Comida, id=comida_id, emprendedor=request.user.emprendedor)
        
        # Eliminar la imagen asociada con la comida, si existe
        if comida.imagen and os.path.isfile(comida.imagen.path):
            os.remove(comida.imagen.path)
        
        comida.delete()  # Elimina la instancia de Comida
        
        messages.success(request, "Comida eliminada correctamente.")
        return redirect('Menu', username=username)
    else:
        messages.error(request, "No se puede eliminar la comida.")
        return redirect('Menu', username=username)