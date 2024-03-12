from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ImagenEventoFormSet, ComidaForm, SobreNosForm, ImagenSobreNosFormSet, ContactoForm, ImagenContactoFormSet, EmprendedorRegisterForm, EmprendimientoForm, ImagenSobreNosForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, ImagenEvento, Comida, Emprendimiento, Emprendedor, ImagenContacto, Contacto, SobreNos, ImagenSobreNos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import CustomLoginForm
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseNotAllowed
import os
from django.contrib.auth.models import User
from itertools import groupby
from operator import attrgetter

# para serialiara  traves de la API
from rest_framework import viewsets
from .serializers import EmprendimientoSerializer
# fin para serializar  traves de la API

from django.forms import inlineformset_factory


# La vista personalizada para el inicio de sesión
class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        # Después de iniciar sesión, en lugar de ir al perfil del usuario,
        # vamos a redirigirlo a la lista de sus emprendimientos.
        return reverse_lazy('emprendimientoListar', kwargs={'username': self.request.user.username})


# La vista del perfil de usuario
@login_required
def user_profile(request, username):
    # Asegúrate de que el nombre de usuario en la URL coincida con el usuario logueado
    if username != request.user.username:
        return redirect('user_profile', username=request.user.username)
    return render(request, 'user_profile.html', {'username': username})

# Vista de registro
def register(request):
    if request.method == 'POST':
        formulario_registro = EmprendedorRegisterForm(request.POST)
        if formulario_registro.is_valid():
            user = formulario_registro.save()
            login(request, user)
            # Redirigir a 'misEmprendimientos' después de registrar usuario y emprendedor.
            return redirect(reverse('emprendimientoListar', kwargs={'username': user.username}))
    else:
        formulario_registro = EmprendedorRegisterForm()
    return render(request, 'register.html', {'miFormularioRegistroUsuario': formulario_registro})

# visa para cerrar sesion
def logout_page(request):
    return render(request, 'logout_page.html')

# vista para poder ver los emprendimientos
# la cambie de nombre de mi emprendimientos
@login_required
def emprendimientoListar(request, username):
    # Asegúrate de que el usuario accediendo a la página es el mismo que el 'username' en la URL.
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)
    
    # Obtén todos los emprendimientos asociados al usuario.
    emprendimientos = Emprendimiento.objects.filter(emprendedor__user=request.user)
    
    return render(request, 'emprendimientoListar.html', {'emprendimientos': emprendimientos, 'username': username})

# vista agregad
@login_required
def crearEmprendimiento(request, username):
    if request.method == 'POST':
        form = EmprendimientoForm(request.POST, request.FILES)
        if form.is_valid():
            emprendimiento = form.save(commit=False)
            emprendimiento.emprendedor = request.user.emprendedor  # Asegúrate de que esta relación exista
            emprendimiento.save()
            return redirect('emprendimientoHome', username=username, nombreEmprendimiento=emprendimiento.nombre)
    else:
        form = EmprendimientoForm()
    return render(request, 'emprendimientoCrear.html', {'miFormularioCrearEmprendimiento': form})


# pagina de inicio despues de logueo de usuario y emprendimiento
# vista agregada
def emprendimientoHome(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    
    # Ejemplo de obtención de productos relacionados con el emprendimiento
    #productos = Producto.objects.filter(emprendimiento=emprendimiento)

    return render(request, 'emprendimientoHome.html', {
        'username': username,
        'emprendimiento': emprendimiento,
        #'productos': productos,  # Añadir productos al contexto
    })


@login_required
def detalleEmprendimiento(request, username, emprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=emprendimiento.nombre, emprendedor__user__username=username)
    return render(request, 'emprendimientoDetalle.html', {'emprendimiento': emprendimiento})


# para agregar un emprendimiento despues de registrarse o iniciar sesion
@login_required
def emprendimientoAgregar(request, username):
    if request.user.username != username:
        return redirect('login')
    
    emprendedor_instance = get_object_or_404(Emprendedor, user=request.user)
    
    if request.method == 'POST':
        form = EmprendimientoForm(request.POST)
        if form.is_valid():
            emprendimiento = form.save(commit=False)
            emprendimiento.emprendedor = emprendedor_instance
            emprendimiento.save()
            return redirect('emprendimientoHome', username=username, nombreEmprendimiento=emprendimiento.nombre)
    else:
        form = EmprendimientoForm()
    
    context = {'miFormularioNuevoEmprendimiento': form}
    return render(request, 'emprendimientoAgregar.html', context)


@login_required
def subirSobreNos(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    if request.method == 'POST':
        form = SobreNosForm(request.POST)
        formset = ImagenSobreNosFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            sobreNos = form.save(commit=False)
            sobreNos.emprendimiento = emprendimiento
            sobreNos.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.sobreNos = sobreNos
                instance.save()
            return redirect('sobreNosDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = SobreNosForm()
        formset = ImagenSobreNosFormSet()
    return render(request, 'sobreNosSubir.html', {
        'miFormularioSobreNos': form,
        'miFormularioImagenesSobreNos': formset,
        'emprendimiento': emprendimiento,
        'username': username,
    })


@login_required
def detalleSobreNos(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    sobreNos = get_object_or_404(SobreNos, emprendimiento=emprendimiento)
    imagenes = sobreNos.imagenesSobreNos.all()
    return render(request, 'sobreNosDetalle.html', {
        'sobreNos': sobreNos,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento
    })

@login_required
def actualizarSobreNos(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    sobreNos, created = SobreNos.objects.get_or_create(emprendimiento=emprendimiento)

    ImagenSobreNosFormSet = inlineformset_factory(SobreNos, ImagenSobreNos, form=ImagenSobreNosForm, extra=4, can_delete=True)
    
    if request.method == 'POST':
        form = SobreNosForm(request.POST, instance=sobreNos)
        formset = ImagenSobreNosFormSet(request.POST, request.FILES, instance=sobreNos)
        
        if form.is_valid() and formset.is_valid():
            form.save()

            # Procesar las instancias del formset para eliminar las imágenes marcadas para borrado
            for form in formset.deleted_forms:
                if form.instance.pk:
                    # Esto elimina el archivo del sistema de archivos y la instancia de la base de datos
                    form.instance.delete()

            formset.save()
            return redirect('sobreNosDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = SobreNosForm(instance=sobreNos)
        formset = ImagenSobreNosFormSet(instance=sobreNos)

    return render(request, 'sobreNosSubir.html', {
        'miFormularioSobreNos': form,
        'miFormularioImagenesSobreNos': formset,
        'sobreNos': sobreNos,
        'emprendimiento': emprendimiento
    })

@login_required
def menu(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    comidas_list = Comida.objects.filter(emprendimiento=emprendimiento).order_by('categoria')
    comidas_por_categoria = {k: list(v) for k, v in groupby(comidas_list, key=attrgetter('categoria'))}

    return render(request, 'menu.html', {
        'username': username,
        'comidas_por_categoria': comidas_por_categoria,
        'emprendimiento': emprendimiento
    })

@login_required
def subirComida(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)

    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES)
        if form.is_valid():
            comida = form.save(commit=False)
            comida.emprendimiento = emprendimiento
            comida.save()
            return redirect('menu', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        # El campo 'emprendimiento' se establece automáticamente en la vista, oculto para el usuario.
        form = ComidaForm(initial={'emprendimiento': emprendimiento})
    
    return render(request, 'comidaSubir.html', {
        'username': username,
        'miFormularioComida': form,
        'emprendimiento': emprendimiento
    })


@login_required
def detalleComida(request, username, nombreEmprendimiento, id):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    comida = get_object_or_404(Comida, id=id, emprendimiento=emprendimiento)
    return render(request, 'comidaDetalle.html', {
        'comida': comida,
        'username': username,
        'emprendimiento': emprendimiento,
    })



@login_required
def actualizarComida(request, username, nombreEmprendimiento, id):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    comida = get_object_or_404(Comida, id=id, emprendimiento=emprendimiento)
    
    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('menu', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = ComidaForm(instance=comida)
    
    return render(request, 'comidaActualizar.html', {
        'username': username,
        'miFormularioComida': form,
        'comida': comida,
        'emprendimiento': emprendimiento
    })

@login_required
def galeria(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    eventos_list = Evento.objects.filter(emprendimiento=emprendimiento).order_by('categoria')
    eventos_por_categoria = {k: list(v) for k, v in groupby(eventos_list, key=attrgetter('categoria'))}

    return render(request, 'galeria.html', {
        'username': username,
        'eventos_por_categoria': eventos_por_categoria,
        'emprendimiento': emprendimiento
    })


@login_required
def subirEvento(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    if request.method == 'POST':
        form = EventoForm(request.POST)
        formset = ImagenEventoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            evento = form.save(commit=False)
            evento.emprendimiento = emprendimiento
            evento.save()
            instances = formset.save(commit=False)
            for instance in instances:
                instance.evento = evento
                instance.save()
            return redirect('galeria', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = EventoForm()
        formset = ImagenEventoFormSet()
    return render(request, 'eventoSubir.html', {
        'miFormularioEvento': form,
        'miFormularioImagenesEvento': formset,
        'username': username,
        'emprendimiento': emprendimiento
    })


@login_required
def detalleEvento(request, username, nombreEmprendimiento, id):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    evento = get_object_or_404(Evento, id=id, emprendimiento=emprendimiento)
    imagenes = evento.imagenesEvento.all()
    
    return render(request, 'eventoDetalle.html', {
        'username': username,
        'evento': evento,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento
    })

@login_required
def actualizarEvento(request, username, nombreEmprendimiento, id):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    evento = get_object_or_404(Evento, id=id, emprendimiento=emprendimiento)
    formset = ImagenEventoFormSet(queryset=ImagenEvento.objects.filter(evento=evento))
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        formset = ImagenEventoFormSet(request.POST, request.FILES, queryset=ImagenEvento.objects.filter(evento=evento))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('galeria', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'eventoActualizar.html', {
        'username': username,
        'miFormularioEvento': form,
        'miFormularioImagenesEvento': formset,
        'evento': evento,
        'emprendimiento': emprendimiento
    })

@login_required
def subirContacto(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        formset = ImagenContactoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            contacto = form.save(commit=False)
            contacto.emprendimiento = emprendimiento
            contacto.save()
            for form in formset:
                imagen_contacto = form.save(commit=False)
                imagen_contacto.contacto = contacto
                imagen_contacto.save()
            return redirect('contactoDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = ContactoForm()
        formset = ImagenContactoFormSet()
    return render(request, 'contactoSubir.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'username': username,
        'emprendimiento': emprendimiento,
    })

@login_required
def detalleContacto(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    contacto = get_object_or_404(Contacto, emprendimiento=emprendimiento)
    imagenes = contacto.imagenesContacto.all()
    return render(request, 'contactoDetalle.html', {
        'contacto': contacto,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento,
    })

@login_required
def actualizarContacto(request, username, nombreEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, nombre=nombreEmprendimiento, emprendedor__user__username=username)
    contacto, created = Contacto.objects.get_or_create(emprendimiento=emprendimiento)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        formset = ImagenContactoFormSet(request.POST, request.FILES, instance=contacto)
        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            formset.save()
            return redirect('contactoDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento)
    else:
        form = ContactoForm(instance=contacto)
        formset = ImagenContactoFormSet(instance=contacto)
    return render(request, 'contactoActualizar.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'contacto': contacto,
        'emprendimiento': emprendimiento,
    })

# para serializar los datos en el api
class EmprendimientoViewSet(viewsets.ModelViewSet):
    queryset = Emprendimiento.objects.all()
    serializer_class = EmprendimientoSerializer