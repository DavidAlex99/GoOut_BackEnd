from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, CategoriaEventoForm, ImagenEventoForm, ComidaForm, CategoriaComidaForm, SobreNosForm, ImagenSobreNosFormSet, ContactoForm, EmprendedorRegisterForm, EmprendimientoForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, CategoriaEvento, ImagenEvento, Comida, CategoriaComida, Emprendimiento, Emprendedor, Contacto, SobreNos
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
from django.contrib.auth.models import User

# para serialiara  traves de la API
from rest_framework import viewsets
from .serializers import EmprendimientoSerializer, EmprendedorSerializer
# fin para serializar  traves de la API

from django.forms import inlineformset_factory

ImagenEventoFormSet = inlineformset_factory(
    Evento, ImagenEvento, form=ImagenEventoForm, extra=3
)



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
        formulario_servicio = EmprendedorRegisterForm(request.POST)
        if formulario_servicio.is_valid():
            user = formulario_servicio.save()
            login(request, user)
            return redirect('crearEmprendimiento', username=user.username)
    else:
        formulario_servicio = EmprendedorRegisterForm()
    return render(request, 'register.html', {'miFormularioRegistroUsuario': formulario_servicio})

# registro del nuevo emprendimiento@login_required
def crearEmprendimiento(request, username):
    # Asegúrate de que el nombre de usuario coincida con el usuario que ha iniciado sesión
    if request.user.username != username:
        return redirect('Menu', username=username) 
    
    # Obtiene o crea el perfil de emprendedor
    emprendedor, created = Emprendedor.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        formulario_servicio = EmprendimientoForm(request.POST)
        if formulario_servicio.is_valid():
            emprendimiento = formulario_servicio.save(commit=False)
            emprendimiento.emprendedor = emprendedor
            emprendimiento.save()
            return redirect('user_profile', username=username)
    else:
        formulario_servicio = EmprendimientoForm()

    return render(request, 'crearEmprendimiento.html', {'miFormularioCrearEmprendimiento': formulario_servicio})

@login_required
def actualizarEmprendimiento(request, username):
    # Asegúrate de que el usuario que hace la solicitud es el mismo que el del username en la URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    # Obtiene el perfil de emprendedor basado en el usuario que ha iniciado sesión.
    user = get_object_or_404(User, username=username)
    emprendedor = get_object_or_404(Emprendedor, user=user)

    # Intenta obtener el emprendimiento asociado con el emprendedor. Si no existe, crea uno nuevo.
    emprendimiento, created = Emprendimiento.objects.get_or_create(emprendedor=emprendedor)

    if request.method == 'POST':
        form = EmprendimientoForm(request.POST, request.FILES, instance=emprendimiento)
        if form.is_valid():
            form.save()
            return redirect('Menu', username=username) 
    else:
        form = EmprendimientoForm(instance=emprendimiento)

    context = {
        'form': form,
        'emprendimiento': emprendimiento,
    }
    return render(request, 'actualizarEmprendimiento.html', context)

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

def detalleSobreNos(request, username):
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
    return render(request, "detalleSobreNos.html", {'miFormularioSobreNos': formulario_servicio})

@login_required
def detalleSobreNos(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    emprendedor = get_object_or_404(Emprendedor, user=request.user)
    sobreNos = get_object_or_404(SobreNos, emprendedor=emprendedor)

    context = {
        'sobreNos': sobreNos,
        'username': username,
    }
    return render(request, 'detalleSobreNos.html', context)

@login_required
def subirSobreNos(request, username):
    emprendedor = get_object_or_404(Emprendedor, user=request.user)

    # Verifica si ya existe información sobre nosotros para este emprendedor
    try:
        sobreNos = SobreNos.objects.get(emprendedor=emprendedor)
        # Si existe, redirige al usuario a la vista de detalles de Sobre Nosotros
        return redirect('detalleSobreNos', username=username)
    except SobreNos.DoesNotExist:
        # Si no existe, permite al usuario crearla
        if request.method == 'POST':
            form = SobreNosForm(request.POST)
            formset = ImagenSobreNosFormSet(request.POST, request.FILES)
            if form.is_valid() and formset.is_valid():
                sobreNos = form.save(commit=False)
                sobreNos.emprendedor = emprendedor
                sobreNos.save()
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.sobreNos = sobreNos
                    instance.save()
                return redirect('detalleSobreNos', username=username)  # Redirige a los detalles después de crear
        else:
            form = SobreNosForm()
            formset = ImagenSobreNosFormSet()

    return render(request, 'subirSobreNos.html', {'miFormularioSobreNos': form, 'miFormularioImagenesSobreNos': formset})


@login_required
def actualizarSobreNos(request, username):
    # Asegúrate de que el usuario que hace la solicitud es el mismo que el del username en la URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    emprendedor = get_object_or_404(Emprendedor, user=request.user)
    sobreNos, created = SobreNos.objects.get_or_create(emprendedor=emprendedor)

    if request.method == 'POST':
        form = SobreNosForm(request.POST, instance=sobreNos)
        formset = ImagenSobreNosFormSet(request.POST, request.FILES, instance=sobreNos)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('detalle_sobre_nos', username=username)  # Asume que tienes una vista para ver los detalles de SobreNos
    else:
        form = SobreNosForm(instance=sobreNos)
        formset = ImagenSobreNosFormSet(instance=sobreNos)

    context = {
        'miFormularioSobreNos': form,
        'miFormularioImagenesSobreNos': formset,
        'sobreNos': sobreNos,
    }
    return render(request, 'actualizarSobreNos.html', context)

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

@login_required
def subirContacto(request, username):
    # Se asegura que el usuario logueado es el mismo que el username en la URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    emprendedor = request.user.emprendedor
    try:
        contacto = Contacto.objects.get(emprendedor=emprendedor)
        # Si el contacto ya existe, redirige a la vista de actualizarContacto.
        return redirect('actualizarContacto', username=username)
    except Contacto.DoesNotExist:
        # Si no existe un objeto Contacto, se procede a crear uno nuevo.
        if request.method == 'POST':
            formulario_servicio = ContactoForm(request.POST, request.FILES)
            if formulario_servicio.is_valid():
                contacto = formulario_servicio.save(commit=False)
                contacto.emprendedor = emprendedor
                contacto.save()
                return redirect('detalle_contacto', username=username)  # Asume una vista de detalle para Contacto.
            else:
                print(formulario_servicio.errors)
        else:
            formulario_servicio = ContactoForm()

    return render(request, "subirContacto.html", {'miFormularioContacto': formulario_servicio})

@login_required
def actualizarContacto(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    # Asume que cada emprendedor tiene un único objeto de contacto asociado.
    emprendedor = get_object_or_404(Emprendedor, user=request.user)
    contacto, created = Contacto.objects.get_or_create(emprendedor=emprendedor)

    if request.method == 'POST':
        form = ContactoForm(request.POST, request.FILES, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('detalle_contacto', username=username)  # Asume que tienes una vista para ver los detalles del contacto
    else:
        form = ContactoForm(instance=contacto)

    context = {
        'form': form,
        'contacto': contacto,
    }
    return render(request, 'actualizarContacto.html', context)


# vista para la galeria
def galeria(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    # aqui se renderizaran los eventos de la base de datos de acuerdoal emprendedor
    emprendedor = request.user.emprendedor
    categoriasEvento = CategoriaEvento.objects.filter(emprendedor=emprendedor)
    eventos = Evento.objects.filter(emprendedor=emprendedor)
    context = {
        # los elementos de la bbdd que se van a renderizar
        "categoriasEvento": categoriasEvento,
        "eventos": eventos,
        "username": username,
    }
    return render(request, "galeria.html", context)

# para visualizar mas detalles del evento que se ha elegido
@login_required
def detalleEvento(request, username, evento_id):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    evento = get_object_or_404(Evento, id=evento_id, emprendedor=request.user.emprendedor)
    imagenes = evento.imagenesEvento.all()  # Asumiendo que tienes un related_name='imagenes' en tu modelo ImagenEvento

    context = {
        'evento': evento,
        'imagenes': imagenes,
        'username': username,
    }
    return render(request, 'detalle_evento.html', context)

# para los formularios para subir imagen 
def subirEvento(request, username):

    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    emprendedor = request.user.emprendedor

    if request.method == "POST":
        formulario_servicio = EventoForm(request.POST, request.FILES, emprendedor=emprendedor) 
        formset = ImagenEventoFormSet(request.POST, request.FILES)

        if formulario_servicio.is_valid() and formset.is_valid():
            evento = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            evento.emprendedor = emprendedor  # Asigna el usuario logueado al objeto comida
            evento.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            
            # Guarda cada una de las imágenes asociadas con el evento
            # Ahora guardamos el formset
            imagenes = formset.save(commit=False)
            for imagen in imagenes:
                imagen.evento = evento
                imagen.save()
            
            return redirect('Galeria', username=username) 
        else:
            print(formulario_servicio.errors, formset.errors)
    else:
        formulario_servicio = EventoForm(emprendedor=emprendedor)
        formset = ImagenEventoFormSet()

    return render(request, "subirEvento.html", {'miFormularioEvento': formulario_servicio, 'miFormularioImagenesEvento': formset})

def subirCategoriaEvento(request, username):
    # Asegúrate de que el usuario logueado es el mismo que el del URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    if request.method == "POST":
        formulario_servicio = CategoriaEventoForm(request.POST, request.FILES) 
        if formulario_servicio.is_valid():
            categoriaEvento = formulario_servicio.save(commit=False)  # Guarda el formulario pero no el objeto
            categoriaEvento.emprendedor = request.user.emprendedor  # Asigna el usuario logueado al objeto comida
            categoriaEvento.save()  # Ahora guarda el objeto comida con el emprendedor asignado
            return redirect('Galeria', username=username) 
        else:
            print(formulario_servicio.errors)
    else:
        formulario_servicio = CategoriaComidaForm()
    return render(request, "subirCategoriaEvento.html", {'miFormularioCategoriaEvento': formulario_servicio})

@login_required
def eliminarCategoriaEvento(request, username, categoriaEvento_id):
    # Solo permitir esta acción si el método es POST y el usuario está autenticado
    if request.method == "POST" and request.user.username == username:
        categoria = get_object_or_404(CategoriaEvento, id=categoriaEvento_id, emprendedor=request.user.emprendedor)
        
         # Eliminar las imágenes de los alimentos asociados a la categoría
        eventos = Evento.objects.filter(categoriaEvento=categoria)
        for evento in eventos:
            if evento.imagen and os.path.isfile(evento.imagen.path):
                os.remove(evento.imagen.path)
            evento.delete()  # Eliminar la instancia de Comida

        # Eliminar la imagen de la categoría
        if categoria.imagen and os.path.isfile(categoria.imagen.path):
            os.remove(categoria.imagen.path)
        
        categoria.delete()  # Eliminar la instancia de CategoriaComida
        messages.success(request, "Categoría y eventos asociados eliminados correctamente.")
        return redirect('Galeria', username=username)

    else:
        messages.error(request, "No se puede eliminar la categoría.")
        return redirect('Galeria', username=username)

@login_required
def eliminarEvento(request, username, evento_id):

    # Asegúrate de que el método es POST y que el usuario está autenticado
    if request.method == "POST" and request.user.username == username:
        evento = get_object_or_404(Evento, id=evento_id, emprendedor=request.user.emprendedor)
        
        # Obtener todas las imágenes asociadas con el evento
        imagenes_evento = ImagenEvento.objects.filter(evento=evento)
        for imagen in imagenes_evento:
            # Eliminar la imagen del sistema de archivos
            if imagen.imagen and os.path.isfile(imagen.imagen.path):
                os.remove(imagen.imagen.path)
            # Eliminar la instancia de imagen de la base de datos
            imagen.delete()
        
        evento.delete()  # Elimina la instancia de Comida
        
        messages.success(request, "Evento y sus imágenes asociadas han sido eliminados.")
        return redirect('Galeria', username=username)
    else:
        messages.error(request, "No se puede eliminar el evento.")
        return redirect('Galeria', username=username)


# vistas para serializaraa traves y consumo de la API
class EmprendimientoViewSet(viewsets.ModelViewSet):
    queryset = Emprendimiento.objects.all()
    serializer_class = EmprendimientoSerializer

class EmprendedorViewSet(viewsets.ModelViewSet):
    queryset = Emprendedor.objects.all()
    serializer_class = EmprendedorSerializer