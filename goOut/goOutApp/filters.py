# dirigido para permitir los filtros, tambien e flutter
import django_filters
from .models import Comida, Evento

class ComidaFilter(django_filters.FilterSet):
    class Meta:
        model = Comida
        fields = ['categoria', 'emprendimiento__nombre']  

class EventoFilter(django_filters.FilterSet):
    class Meta:
        model = Evento
        fields = ['categoria', 'emprendimiento__nombre']