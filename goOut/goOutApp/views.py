from django.shortcuts import render, HttpResponse

# Create your views here.

#
def home(request):
    return render(request, "home.html")

# vista para el menu
def menu(request):
    return render(request, "menu.html")

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
    return render(request, "galeria.html")

def subirComida(request):
    return render(request, "subirComida.html")