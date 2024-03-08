from django.contrib import admin

# Register your models here.
from .models import Comida, Galeria, Evento, Contacto, SobreNos, Emprendedor

# lo que va a aparecer en el admin

class eventoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')
    
class galeriaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class comidaAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class contactoAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class sobreNosAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

class emprendedorAdmin(admin.ModelAdmin):
    readonly_fields=('created', 'updated')

#regisrar alas tablas como las clases
admin.site.register(Evento, eventoAdmin)
admin.site.register(Galeria, galeriaAdmin)
admin.site.register(Comida, comidaAdmin)
admin.site.register(Contacto, contactoAdmin)
admin.site.register(SobreNos, sobreNosAdmin)
admin.site.register(Emprendedor, emprendedorAdmin)