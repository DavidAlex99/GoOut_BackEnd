from django.db import models



#subclases de Galeria
class Imagen(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    archivo = models.ImageField(upload_to='evento')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='imagen_evento')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

# fin subclases de galeria 

class Galeria(models.Model):
    imagenes = models.ManyToManyField(Imagen)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_evento(self, imagen):
        self.imagenes.add(imagen)
        return self.save()

# subclases de menu
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    # como va a aprecer en el panel de administrador
    def __str__(self):
        return self.nombre
    
class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='imagen_comida')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
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

# fin subclases de menu
class Menu(models.Model):
    alimentos = models.ManyToManyField(Alimento)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_alimento(self, alimento):
        self.alimentos.add(alimento)
        return self.save()

class Contacto(models.Model):
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE)
    correo = models.EmailField()
    telefono = models.IntegerField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def llenar_modificar_contacto(self):
        return self.save()

class Ubicacion(models.Model):
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='imagen_ubicacion')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def gurdar_ubicacion(self):
        return self.save()

class SobreNos(models.Model):
    descrpcion = models.TextField()
    imagen = models.ForeignKey(Imagen, on_delete=models.CASCADE, related_name='imagen_sobre_nos')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)

    def agregar_descripcion(self, descripcion):
        self.descrpcion = descripcion
        return self.save()
    
class Emprendedor(models.Model):
    galeria = models.OneToOneField(Galeria, on_delete=models.CASCADE)
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE)
    sobre_nos = models.OneToOneField(SobreNos, on_delete=models.CASCADE)
    contacto = models.OneToOneField(Contacto, on_delete=models.CASCADE)
    ubicacion = models.OneToOneField(Ubicacion, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)