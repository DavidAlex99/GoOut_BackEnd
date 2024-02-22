from django.contrib import admin

# Register your models here.
from .models import Alimento, Categoria, Galeria, Evento, Imagen, Menu, Contacto, Ubicacion, SobreNos, Emprendedor

# lo que va a aparecer en el admin
class imagenAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class eventoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')
    
class galeriaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class categoriaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class alimentoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class menuAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class contactoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class ubicacionAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class sobreNosAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class emprendedorAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

#regisrar alas tablas como las clases
admin.site.register(Imagen, imagenAdmin)
admin.site.register(Evento, eventoAdmin)
admin.site.register(Galeria, galeriaAdmin)
admin.site.register(Categoria, categoriaAdmin)
admin.site.register(Alimento, alimentoAdmin)
admin.site.register(Menu, menuAdmin)
admin.site.register(Contacto, contactoAdmin)
admin.site.register(Ubicacion, ubicacionAdmin)
admin.site.register(SobreNos, sobreNosAdmin)
admin.site.register(Emprendedor, emprendedorAdmin)