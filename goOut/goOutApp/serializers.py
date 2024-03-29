from rest_framework import serializers
from .models import Emprendimiento, Emprendedor, Comida, Evento, ImagenEvento, Contacto, ImagenContacto, SobreNos, ImagenSobreNos, Cliente, Reserva
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

class ImagenEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEvento
        fields = ['imagen', 'created', 'updated']

class EventoSerializer(serializers.ModelSerializer):
    emprendimiento_id = serializers.ReadOnlyField(source='emprendimiento.id')  # Asegúrate de que 'emprendimiento' sea el nombre correcto de la relación
    emprendimiento_nombre = serializers.ReadOnlyField(source='emprendimiento.nombre')
    imagenesEvento = ImagenEventoSerializer(many=True, read_only=True)
    id = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descripcion', 'categoria', 'disponibles', 'precio', 'imagenesEvento', 'created', 'updated', 'emprendimiento_id', 'emprendimiento_nombre']

# para serilizar plazas de eventos
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['evento', 'cantidad']  # Simplificado para el propósito de la reserva

    def create(self, validated_data):
        # Asumiendo que el usuario autenticado está disponible como self.context['request'].user
        user = self.context['request'].user
        cliente = Cliente.objects.get(user=user)

        # Si 'cliente' está en validated_data, lo eliminamos ya que lo estableceremos manualmente.
        validated_data.pop('cliente', None)

        # Crea la reserva con el cliente recuperado.
        reserva = Reserva.objects.create(**validated_data, cliente=cliente)
        return reserva
# fin para serilizar plazas de eventos

class ImagenContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenContacto
        fields = ['imagen', 'created', 'updated']

class ContactoSerializer(serializers.ModelSerializer):
    imagenesContacto = ImagenContactoSerializer(many=True, read_only=True)

    class Meta:
        model = Contacto
        fields = ['descripcion', 'direccion', 'correo', 'telefono', 'latitud', 'longitud', 'imagenesContacto', 'created', 'updated']

class ImagenSobreNosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenSobreNos
        fields = ['imagen', 'created', 'updated']

class SobreNosSerializer(serializers.ModelSerializer):
    imagenesSobreNos = ImagenSobreNosSerializer(many=True, read_only=True)

    class Meta:
        model = SobreNos
        fields = ['descripcion', 'imagenesSobreNos', 'created', 'updated']

class ComidaSerializer(serializers.ModelSerializer):
    emprendimiento_id = serializers.ReadOnlyField(source='emprendimiento.id')
    
    class Meta:
        model = Comida
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'categoria', 'created', 'updated', 'emprendimiento_id']

class EmprendimientoSerializer(serializers.ModelSerializer):
    eventos = EventoSerializer(source='evento_set', many=True, read_only=True)
    contacto = ContactoSerializer(read_only=True)
    sobreNos = SobreNosSerializer(read_only=True)
    comidas = ComidaSerializer(source='comida_set', many=True, read_only=True)  # No es necesario usar source='comida_set' si ya está usando el nombre predeterminado

    class Meta:
        model = Emprendimiento
        fields = ['nombre', 'descripcion', 'categoria', 'imagen', 'eventos', 'contacto', 'sobreNos', 'comidas', 'created', 'updated']

# paso 2: registro e inicio de sesion para este caso desde flutter
# serializador para el registro de usuarios e inicio de sesion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
# serializador para actualizacion de los campos de cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['telefono']
