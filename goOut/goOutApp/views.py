from django.shortcuts import render, HttpResponse, redirect
from .forms import EventoForm, ImagenEventoFormSet, ComidaForm, SobreNosForm, ImagenSobreNosFormSet, ContactoForm, ImagenContactoFormSet, EmprendedorRegisterForm, EmprendimientoForm, ImagenSobreNosForm
# importacion de modelos para la visualizacion de los registros en la bbdd
from .models import Evento, ImagenEvento, Comida, Emprendimiento, Emprendedor, ImagenContacto, Contacto, SobreNos, ImagenSobreNos, Cliente, Reserva
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
from .serializers import EmprendimientoSerializer, ComidaSerializer, EventoSerializer, UserSerializer, ReservaSerializer
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ComidaFilter, EventoFilter
from rest_framework.response import Response    


# para el registro de usuario
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login 
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
# fin para el registro de usuario

# para serializar comidas, eventos, get emprendimiento
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
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
            return redirect('emprendimientoHome', username=username, nombreEmprendimiento=emprendimiento.nombre, id=emprendimiento.nombre)
    else:
        form = EmprendimientoForm()
    return render(request, 'emprendimientoCrear.html', {'miFormularioCrearEmprendimiento': form})


# pagina de inicio despues de logueo de usuario y emprendimiento
# vista agregada
def emprendimientoHome(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    print("SobreNos exists:", sobreNos_exists)
    # Ejemplo de obtención de productos relacionados con el emprendimiento
    #productos = Producto.objects.filter(emprendimiento=emprendimiento)

    return render(request, 'emprendimientoHome.html', {
        'username': username,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
        #'productos': productos,  # Añadir productos al contexto
    })

# no estoy seguro si pasar el id del emprendimiento
@login_required
def detalleEmprendimiento(request, username, emprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    return render(request, 'emprendimientoDetalle.html', {
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })


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
            return redirect('emprendimientoHome', username=username, nombreEmprendimiento=emprendimiento.nombre, idEmprendimiento=emprendimiento.id)
    else:
        form = EmprendimientoForm()
    
    context = {'miFormularioNuevoEmprendimiento': form}
    return render(request, 'emprendimientoAgregar.html', context)


@login_required
def subirSobreNos(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    contacto_exists = hasattr(emprendimiento, 'contacto')

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
            return redirect('sobreNosDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = SobreNosForm()
        formset = ImagenSobreNosFormSet()
    return render(request, 'sobreNosSubir.html', {
        'miFormularioSobreNos': form,
        'miFormularioImagenesSobreNos': formset,
        'emprendimiento': emprendimiento,
        'username': username,
        'contacto_exists': contacto_exists,
    })


@login_required
def detalleSobreNos(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos = get_object_or_404(SobreNos, emprendimiento=emprendimiento)
    imagenes = sobreNos.imagenesSobreNos.all()
    contacto_exists = hasattr(emprendimiento, 'contacto')
    return render(request, 'sobreNosDetalle.html', {
        'sobreNos': sobreNos,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento,
        'contacto_exists': contacto_exists,
    })

@login_required
def actualizarSobreNos(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos, created = SobreNos.objects.get_or_create(emprendimiento=emprendimiento)

    ImagenSobreNosFormSet = inlineformset_factory(SobreNos, ImagenSobreNos, form=ImagenSobreNosForm, extra=4, can_delete=True)

    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    
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
            return redirect('sobreNosDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = SobreNosForm(instance=sobreNos)
        formset = ImagenSobreNosFormSet(instance=sobreNos)

    return render(request, 'sobreNosSubir.html', {
        'miFormularioSobreNos': form,
        'miFormularioImagenesSobreNos': formset,
        'sobreNos': sobreNos,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def menu(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    comidas_list = Comida.objects.filter(emprendimiento=emprendimiento).order_by('categoria')
    comidas_por_categoria = {k: list(v) for k, v in groupby(comidas_list, key=attrgetter('categoria'))}
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')

    return render(request, 'menu.html', {
        'username': username,
        'comidas_por_categoria': comidas_por_categoria,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def subirComida(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')

    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES)
        if form.is_valid():
            comida = form.save(commit=False)
            comida.emprendimiento = emprendimiento
            comida.save()
            return redirect('menu', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        # El campo 'emprendimiento' se establece automáticamente en la vista, oculto para el usuario.
        form = ComidaForm(initial={'emprendimiento': emprendimiento})
    
    return render(request, 'comidaSubir.html', {
        'username': username,
        'miFormularioComida': form,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })


@login_required
def detalleComida(request, username, nombreEmprendimiento, idEmprendimiento, idComida):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    comida = get_object_or_404(Comida, id=idComida, emprendimiento=emprendimiento)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    return render(request, 'comidaDetalle.html', {
        'comida': comida,
        'username': username,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })



@login_required
def actualizarComida(request, username, nombreEmprendimiento, idEmprendimiento, idComida):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    comida = get_object_or_404(Comida, id=idComida, emprendimiento=emprendimiento)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    
    if request.method == 'POST':
        form = ComidaForm(request.POST, request.FILES, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('menu', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = ComidaForm(instance=comida)
    
    return render(request, 'comidaActualizar.html', {
        'username': username,
        'miFormularioComida': form,
        'comida': comida,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def galeria(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    eventos_list = Evento.objects.filter(emprendimiento=emprendimiento).order_by('categoria')
    eventos_por_categoria = {k: list(v) for k, v in groupby(eventos_list, key=attrgetter('categoria'))}
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')

    return render(request, 'galeria.html', {
        'username': username,
        'eventos_por_categoria': eventos_por_categoria,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })


@login_required
def subirEvento(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
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
            return redirect('galeria', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = EventoForm()
        formset = ImagenEventoFormSet()
    return render(request, 'eventoSubir.html', {
        'miFormularioEvento': form,
        'miFormularioImagenesEvento': formset,
        'username': username,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })


@login_required
def detalleEvento(request, username, nombreEmprendimiento, idEmprendimiento, idEvento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    evento = get_object_or_404(Evento, id=idEvento, emprendimiento=emprendimiento)
    imagenes = evento.imagenesEvento.all()
    reservas = evento.reservas.all()
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')

    return render(request, 'eventoDetalle.html', {
        'username': username,
        'evento': evento,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento,
        'reservas': reservas, 
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def actualizarEvento(request, username, nombreEmprendimiento, idEmprendimiento, idEvento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    evento = get_object_or_404(Evento, id=idEvento, emprendimiento=emprendimiento)
    formset = ImagenEventoFormSet(queryset=ImagenEvento.objects.filter(evento=evento))
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        formset = ImagenEventoFormSet(request.POST, request.FILES, queryset=ImagenEvento.objects.filter(evento=evento))
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('galeria', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = EventoForm(instance=evento)
    
    return render(request, 'eventoActualizar.html', {
        'username': username,
        'miFormularioEvento': form,
        'miFormularioImagenesEvento': formset,
        'evento': evento,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def verReservasEvento(request, username, nombreEmprendimiento, idEmprendimiento, idEvento):
    # Asegúrate de que el usuario actual es el dueño del emprendimiento
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    evento = get_object_or_404(Evento, id=idEvento, emprendimiento=emprendimiento)
    reservas = Reserva.objects.filter(evento=evento).select_related('cliente')
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')
    
    return render(request, 'eventoReservas.html', {
        'evento': evento,
        'reservas': reservas,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

@login_required
def subirContacto(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')

    if request.method == 'POST':
        form = ContactoForm(request.POST)
        formset = ImagenContactoFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            contacto = form.save(commit=False)
            contacto.latitud = request.POST.get('latitud')  # Obtener latitud del POST
            contacto.longitud = request.POST.get('longitud')  # Obtener longitud del POST
            contacto.emprendimiento = emprendimiento
            contacto.save()
            for form in formset:
                if form.cleaned_data.get('imagen'):  # Verifica si hay imagen
                    imagen_contacto = form.save(commit=False)
                    imagen_contacto.contacto = contacto
                    imagen_contacto.save()
            return redirect('contactoDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = ContactoForm()
        formset = ImagenContactoFormSet()

    return render(request, 'contactoSubir.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'username': username,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
    })


@login_required
def detalleContacto(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    contacto = get_object_or_404(Contacto, emprendimiento=emprendimiento)
    imagenes = contacto.imagenesContacto.all()
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')

    return render(request, 'contactoDetalle.html', {
        'contacto': contacto,
        'imagenes': imagenes,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
    })

@login_required
def actualizarContacto(request, username, nombreEmprendimiento, idEmprendimiento):
    emprendimiento = get_object_or_404(Emprendimiento, id=idEmprendimiento, emprendedor__user__username=username)
    contacto, created = Contacto.objects.get_or_create(emprendimiento=emprendimiento)
    sobreNos_exists = hasattr(emprendimiento, 'sobreNos')
    contacto_exists = hasattr(emprendimiento, 'contacto')

    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        formset = ImagenContactoFormSet(request.POST, request.FILES, instance=contacto)
        if form.is_valid() and formset.is_valid():
            form.save()
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            formset.save()
            return redirect('contactoDetalle', username=username, nombreEmprendimiento=nombreEmprendimiento, idEmprendimiento=idEmprendimiento)
    else:
        form = ContactoForm(instance=contacto)
        formset = ImagenContactoFormSet(instance=contacto)
    return render(request, 'contactoActualizar.html', {
        'miFormularioContacto': form,
        'miFormularioImagenesContacto': formset,
        'contacto': contacto,
        'emprendimiento': emprendimiento,
        'sobreNos_exists': sobreNos_exists,
        'contacto_exists': contacto_exists,
    })

# para serializar los datos en el api y que permita el filtro de emprendimiento
class EmprendimientoViewSet(viewsets.ModelViewSet):
    queryset = Emprendimiento.objects.all()
    serializer_class = EmprendimientoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categoria', 'emprendedor__nombre']

# para que permita el filtro de comidas, la logica de fltro esta en filters,py
class ComidaViewSet(viewsets.ModelViewSet):
    queryset = Comida.objects.all()
    serializer_class = ComidaSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ComidaFilter

# para que permita el filtro de eventos, la logica de fltro esta en filters,py
class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = EventoFilter

# para la funcionalidad de reservas
from rest_framework.exceptions import ValidationError

# -------------------- RESERVAS ------------------------------
class CrearReserva(generics.CreateAPIView):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def perform_create(self, serializer):
        evento_id = serializer.validated_data['evento'].id
        evento = get_object_or_404(Evento, id=evento_id)
        cantidad_reservada = serializer.validated_data['cantidad']
        
        if evento.disponibles < cantidad_reservada:
            raise ValidationError('No hay suficientes plazas disponibles para este evento.')

        evento.disponibles -= cantidad_reservada
        evento.save()

        user = self.request.user
        cliente = get_object_or_404(Cliente, user=user)

        serializer.save(cliente=cliente, evento=evento)

    # funccionalidad: devoluciosn de datos de reserva al cliente
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Aquí asumes que serializer.data incluye toda la información que quieres devolver
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# Para permitir que el usuario cancele la reserva que ha realizado
# -------------------- FIN RESERVAS ------------------------------

# para que al selecccionar un evento me lleve a su emprendimiento
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_emprendimiento(request, pk):
    try:
        emprendimiento = Emprendimiento.objects.get(pk=pk)
        serializer = EmprendimientoSerializer(emprendimiento)
        return Response(serializer.data)
    except Emprendimiento.DoesNotExist:
        return Response(status=404)

# paso 1: registro e inicio de sesion para este caso desde flutter
# Vista para registro
@api_view(['POST'])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        telefono = request.data.get('telefono', None)
        if telefono:
            Cliente.objects.create(user=user, telefono=telefono)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)  
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)