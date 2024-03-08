from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# este modelo es el que presetara como uno de los tantos emprendimientos
class Emprendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField()
    nombre = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Emprendimiento(models.Model):
    CATEGORIAS = [
        ('REST', 'Restaurante'),
        ('BAR', 'Bar'),
        ('DISCO', 'Discoteca'),
        ('CAFE', 'Cafetería'),
        ('TIENDA', 'Tienda'),
        ('SERV', 'Servicios'),
        ('OTRO', 'Otro'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS, default='OTRO')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

#subclases de Galeria
class Evento(models.Model):
    CATEGORIAS_EVENTO = [
        ('ARTISTICAS', 'Concierto'),
        ('CULTURALES', 'Teatro'),
        ('DEPORTIVO', 'Deportivo'),
        ('AIRE_LIBRE', 'Aire_libre'),
        ('NOCTURNO', 'Nocturno'),
        ('AUTO_CONTROL', 'Auto_control'),
        ('ACT_FANCY', 'Act_fancy'),
    ]

    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    categoria = models.CharField(max_length=15, choices=CATEGORIAS_EVENTO, default='OTRO')
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)
    disponibles = models.IntegerField()
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.0)])
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class ImagenEvento(models.Model):
    evento = models.ForeignKey(Evento, related_name='imagenesEvento', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen_evento')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen de {self.evento.titulo}"
    
# fin subclases de galeria 

class Galeria(models.Model):
    eventos = models.ManyToManyField(Evento)
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_evento(self, imagen):
        self.imagenes.add(imagen)
        return self.save()

# subclases de menu
class Comida(models.Model):
    CATEGORIAS_COMIDA = [
        ('ENTRANTE', 'Entrante'),
        ('PRINCIPAL', 'Plato Principal'),
        ('POSTRE', 'Postre'),
        ('BEBIDA', 'Bebida'),
        ('SNACKS', 'snacks'),
        ('OTRO', 'Otro'),
    ]
     
    # Atributos existentes
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.0)])
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_comida')
    categoria = models.CharField(max_length=10, choices=CATEGORIAS_COMIDA, default='OTRO')
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def definir_precio(self, precio):
        self.precio = precio
        return self.save()
    
    def definir_categoria(self, categoria):
        self.categoria = categoria
        return self.save()

    def guardar_alimento(self):
        return self.save()
    
    # como aparecera en el panel de administracion
    def __str__(self):
        return self.nombre

class Contacto(models.Model):
    descripcion = models.TextField()
    direccion = models.CharField(max_length=255)
    direccion_secundaria = models.CharField(max_length=255, blank=True, null=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20) 
    # campos que van a servir para el api google maps
    latitud = models.FloatField(null=True, blank=True)  # Nuevo campo para latitud
    longitud = models.FloatField(null=True, blank=True)  # Nuevo campo para longitud
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# multiples imagenes como lugares referenciales etc
class ImagenContacto(models.Model):
    contacto = models.ForeignKey(Contacto, related_name='imagenesContacto', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen_contacto')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class SobreNos(models.Model):
    descripcion = models.TextField()
    emprendimiento = models.ForeignKey(Emprendimiento, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_descripcion(self, descripcion):
        self.descripcion = descripcion  
        return self.save()
    
    def __str__(self):
        return f"Sobre {self.emprendedor.nombre}"  
    
# multiples imagenes como lugares referenciales etc
class ImagenSobreNos(models.Model):
    sobreNos = models.ForeignKey(SobreNos, related_name='imagenesSobreNos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='imagen_sobre_nos')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.sobreNos.emprendedor.nombre}"