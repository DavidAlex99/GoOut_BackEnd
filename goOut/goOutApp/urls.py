"""
URL configuration for gates project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# imortacion de las vistas
from goOutApp import views

from django.conf import settings
from django.conf.urls.static import static
# para el inicio de sesion
from .views import user_profile, CustomLoginView, register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name="Home"),
    path('<str:username>/menu/', views.menu, name="Menu"),
    path('<str:username>/subirComida/', views.subirComida, name="SubirComida"),
    path('<str:username>/subirCategoria/', views.subirCategoria, name="SubirCategoria"),
    path('<str:username>/acerca/', views.acerca, name="Acerca"),
    path('<str:username>/galeria/', views.galeria, name="Galeria"),
    path('<str:username>/subirImagen/', views.subirImagen, name="SubirImagen"),
    path('<str:username>/ubicacion/', views.ubicacion, name="Ubicacion"),
    path('<str:username>/contacto/', views.contacto, name="Contacto"),
    # para el inciio de sesion
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('<str:username>/', user_profile, name='user_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
