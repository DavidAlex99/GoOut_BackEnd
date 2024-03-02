from rest_framework import serializers
from .models import Emprendimiento, Emprendedor, Evento, Comida

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = ['id', 'titulo', 'descripcion', 'categoriaEvento', 'created', 'updated']

class ComidaSerializer(serializers.ModelSerializer):
    imagen = serializers.SerializerMethodField('get_imagen_url')
    class Meta:
        model = Comida
        fields = ['id', 'nombre', 'precio', 'descripcion','imagen', 'categoriaComida', 'created', 'updated']

    def get_imagen_url(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return self.context['request'].build_absolute_uri(obj.imagen.url)
        else:
            return None

# Primero, serializa el modelo Emprendedor si aún no lo has hecho
class EmprendedorSerializer(serializers.ModelSerializer):
    eventos = EventoSerializer(many=True, read_only=True, source='evento_set')
    comidas = ComidaSerializer(many=True, read_only=True, source='comida_set')
    class Meta:
        model = Emprendedor
        fields = '__all__'  # Ajusta los campos según necesites

class EmprendimientoSerializer(serializers.ModelSerializer):
    emprendedor = EmprendedorSerializer(read_only=True)
    
    class Meta:
        model = Emprendimiento
        fields = ['id', 'nombre', 'descripcion', 'emprendedor', 'created', 'updated']

