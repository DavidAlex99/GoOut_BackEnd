from rest_framework import serializers
from .models import Emprendimiento, Emprendedor, Comida, Evento, ImagenEvento, Contacto, ImagenContacto, SobreNos, ImagenSobreNos

class ImagenEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagenEvento
        fields = ['imagen', 'created', 'updated']

class EventoSerializer(serializers.ModelSerializer):
    emprendimiento_id = serializers.ReadOnlyField(source='emprendimiento.id')  # Asegúrate de que 'emprendimiento' sea el nombre correcto de la relación
    emprendimiento_nombre = serializers.ReadOnlyField(source='emprendimiento.nombre')
    imagenesEvento = ImagenEventoSerializer(many=True, read_only=True)

    class Meta:
        model = Evento
        fields = ['titulo', 'descripcion', 'categoria', 'disponibles', 'precio', 'imagenesEvento', 'created', 'updated', 'emprendimiento_id', 'emprendimiento_nombre']

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
    class Meta:
        model = Comida
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'categoria', 'created', 'updated']

class EmprendimientoSerializer(serializers.ModelSerializer):
    eventos = EventoSerializer(source='evento_set', many=True, read_only=True)
    contacto = ContactoSerializer(read_only=True)
    sobreNos = SobreNosSerializer(read_only=True)
    comidas = ComidaSerializer(source='comida_set', many=True, read_only=True)  # No es necesario usar source='comida_set' si ya está usando el nombre predeterminado

    class Meta:
        model = Emprendimiento
        fields = ['nombre', 'descripcion', 'categoria', 'imagen', 'eventos', 'contacto', 'sobreNos', 'comidas', 'created', 'updated']
