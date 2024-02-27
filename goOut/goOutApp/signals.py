# este archivo servira como senal
# es decir que para cuando se cree un usuario, obligatoriamente
# se cree un emprendedor su perdil

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Emprendedor

@receiver(post_save, sender=User)
def crear_perfil_emprendedor(sender, instance, created, **kwargs):
    if created:
        Emprendedor.objects.create(user=instance)

@receiver(post_save, sender=User)
def guardar_perfil_emprendedor(sender, instance, **kwargs):
    instance.emprendedor.save()
