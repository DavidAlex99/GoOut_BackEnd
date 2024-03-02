from rest_framework import serializers
from .models import Emprendimiento, Emprendedor

# Primero, serializa el modelo Emprendedor si aún no lo has hecho
class EmprendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprendedor
        fields = '__all__'  # Ajusta los campos según necesites

class EmprendimientoSerializer(serializers.ModelSerializer):
    emprendedor = EmprendedorSerializer(read_only=True)
    
    class Meta:
        model = Emprendimiento
        fields = ['id', 'nombre', 'descripcion', 'emprendedor', 'created', 'updated']
