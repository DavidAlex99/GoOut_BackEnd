from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# este modelo es el que presetara como uno de los tantos emprendimientos
class Emprendedor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    edad = models.IntegerField()
    nombre = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

class Emprendimiento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

#subclases de Galeria
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_evento')
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# fin subclases de galeria 

class Galeria(models.Model):
    eventos = models.ManyToManyField(Evento)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_evento(self, imagen):
        self.imagenes.add(imagen)
        return self.save()

# subclases de menu
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_categoria')
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    # como va a aprecer en el panel de administrador
    def __str__(self):
        return self.nombre
    
class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.0)])
    descripcion = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagen_comida')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
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
    imagen = models.ImageField(upload_to='imagen_contacto')
    correo = models.EmailField()
    telefono = models.IntegerField()
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def llenar_modificar_contacto(self):
        return self.save()

class Ubicacion(models.Model):
    imagen = models.ImageField(upload_to='imagen_ubicacion')
    direccion = models.CharField(max_length=255)
    direccion_secundaria = models.CharField(max_length=255, blank=True, null=True)
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def gurdar_ubicacion(self):
        return self.save()

class SobreNos(models.Model):
    descrpcion = models.TextField()
    imagen = models.ImageField(upload_to='imagen_sobre_nos')
    emprendedor = models.ForeignKey(Emprendedor, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_descripcion(self, descripcion):
        self.descrpcion = descripcion
        return self.save()
    
