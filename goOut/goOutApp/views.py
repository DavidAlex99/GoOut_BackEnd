from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ComidaForm, CategoriaForm, SobreNosForm, UbicacionForm, ContactoForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, Alimento, Categoria
# Create your views here.

#
def home(request):
    return render(request, "home.html")


def menu(request):
     # aqui se renderizaran los eventos de la base de datos
    categorias = Categoria.objects.all()
    alimentos = Alimento.objects.all()
    context = {
        "categorias": categorias,
        "alimentos": alimentos,
    }
    return render(request, "menu.html", context)


def subirComida(request):
    if request.method == "POST":
        formulario_servicio = ComidaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Menu') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ComidaForm()
    return render(request, "subirComida.html", {'miFormularioComida': formulario_servicio})


def acerca(request):
    if request.method == "POST":
        formulario_servicio = SobreNosForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = SobreNosForm()
    return render(request, "acerca.html", {'miFormularioSobreNos': formulario_servicio})

#vista para el contacto
def contacto(request):
    if request.method == "POST":
        formulario_servicio = ContactoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = ContactoForm()
    return render(request, "contacto.html", {'miFormularioContacto': formulario_servicio})


#vista para la ubicacion
def ubicacion(request):
    if request.method == "POST":
        formulario_servicio = UbicacionForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Home') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = UbicacionForm()
    return render(request, "ubicacion.html", {'miFormularioUbicacion': formulario_servicio})

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
            return redirect('Galeria') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = EventoForm()
    return render(request, "subirGaleria.html", {'miFormularioImagen': formulario_servicio})




def subirCategoria(request):
    if request.method == "POST":
        formulario_servicio = CategoriaForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            formulario_servicio.save()  
            return redirect('Menu') 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = CategoriaForm()
    return render(request, "subirCategoria.html", {'miFormularioCategoria': formulario_servicio})
