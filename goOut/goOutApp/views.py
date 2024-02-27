from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ComidaForm, CategoriaForm, SobreNosForm, UbicacionForm, ContactoForm, EmprendedorRegisterForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, Alimento, Categoria, Emprendedor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import CustomLoginForm
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

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
    categorias = Categoria.objects.filter(emprendedor=emprendedor)
    alimentos = Alimento.objects.filter(emprendedor=emprendedor)
    context = {
        # los elementos de la bbdd que se van a renderizar
        "categorias": categorias,
        "alimentos": alimentos,
    }
    return render(request, "menu.html", context)


def subirComida(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    if request.method == "POST":
        formulario_servicio = ComidaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            comida = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            comida.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            comida.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ComidaForm()
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
def subirImagen(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = EventoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            evento = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            evento.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            evento.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Galeria', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = EventoForm()
    return render(request, "subirGaleria.html", {'miFormularioImagen': formulario_servicio})




def subirCategoria(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = CategoriaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            categoria = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            categoria.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            categoria.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Menu', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = CategoriaForm()
    return render(request, "subirCategoria.html", {'miFormularioCategoria': formulario_servicio})
