from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ComidaForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, Alimento
# Create your views here.

#
def home(request):
    return render(request, "home.html")

# vista para el menu
def menu(request):
    # aqui se renderizaran los eventos de la base de datos
    alimentos = Alimento.objects.all()
    return render(request, "menu.html", {"alimentos": alimentos})

def subirComida(request):
    if request.method == "POST":
        formulario_servicio = ComidaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ComidaForm()
    return render(request, "subirComida.html", {'miFormularioComida': formulario_servicio})

# vista para Sobre Nosotros
def acerca(request):
    return render(request, "acerca.html")

#vista para el contacto
def contacto(request):
    return render(request, "contacto.html")

#vista para la ubicacion
def ubicacion(request):
    return render(request, "ubicacion.html")

# vista para la galeria
def galeria(request):
    # aqui se renderizaran los eventos de la base de datos
    eventos = Evento.objects.all()
    return render(request, "galeria.html", {"eventos": eventos})

# para los formularios para subir imagen 
def subirImagen(request):
    if request.method == "POST":
        formulario_servicio = EventoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = EventoForm()
    return render(request, "subirGaleria.html", {'miFormularioImagen': formulario_servicio})
