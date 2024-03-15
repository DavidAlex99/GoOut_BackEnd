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
from django.urls import path, include, reverse_lazy
# imortacion de las vistas
from goOutApp import views

from django.conf import settings
from django.conf.urls.static import static
# para el inicio de sesion
from .views import user_profile, CustomLoginView, register
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token
# Imports para poder consumir las APIS
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path



router = DefaultRouter()
router.register(r'emprendimientos', views.EmprendimientoViewSet)
router.register(r'comidas', views.ComidaViewSet) 
router.register(r'eventos', views.EventoViewSet) 
# url token autenticacion registro


urlpatterns = [
    # para el inciio de sesion
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('<str:username>/crearEmprendimiento/', views.crearEmprendimiento, name='crearEmprendimiento'),
    path('<str:username>/misEmprendimientos/', views.emprendimientoListar, name='emprendimientoListar'),
    path('<str:username>/<str:nombreEmprendimiento>/home', views.emprendimientoHome, name='emprendimientoHome'),

    path('<str:username>/<str:nombreEmprendimiento>/subirSobreNos/', views.subirSobreNos, name='sobreNosSubir'),
    path('<str:username>/<str:nombreEmprendimiento>/sobreNos/', views.detalleSobreNos, name='sobreNosDetalle'),
    path('<str:username>/<str:nombreEmprendimiento>/subirSobreNos/actualizarSobreNos/', views.actualizarSobreNos, name='sobreNosActualizar'),
    
    path('<str:username>/<str:nombreEmprendimiento>/menu/', views.menu, name='menu'),
    path('<str:username>/<str:nombreEmprendimiento>/menu/subirComida/', views.subirComida, name='comidaSubir'),
    path('<str:username>/<str:nombreEmprendimiento>/menu/<int:id>/', views.detalleComida, name='comidaDetalle'),
    path('<str:username>/<str:nombreEmprendimiento>/menu/<int:id>/actualizarComida/', views.actualizarComida, name='comidaActualizar'),

    path('<str:username>/<str:nombreEmprendimiento>/galeria/', views.galeria, name='galeria'),
    path('<str:username>/<str:nombreEmprendimiento>/galeria/subirEvento/', views.subirEvento, name='eventoSubir'),
    path('<str:username>/<str:nombreEmprendimiento>/galeria/<int:id>/', views.detalleEvento, name='eventoDetalle'),
    path('<str:username>/<str:nombreEmprendimiento>/galeria/<int:id>/actualizarEvento/', views.actualizarEvento, name='eventoActualizar'),

    path('<str:username>/<str:nombreEmprendimiento>/subirContacto/', views.subirContacto, name='contactoSubir'),
    path('<str:username>/<str:nombreEmprendimiento>/contacto/', views.detalleContacto, name='contactoDetalle'),
    path('<str:username>/<str:nombreEmprendimiento>/contacto/actualizar/', views.actualizarContacto, name='contactoActualizar'),

    #url para consumo de API
    path('', include(router.urls)),
    path('emprendimientos/<int:pk>/', views.get_emprendimiento),
    # paso 3: registro e inicio de sesion para este caso desde flutter
    # url para la autenticacion de clientes para recibir un token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('register/', views.register, name='register'),

]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
