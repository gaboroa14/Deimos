from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', ListaEventos.as_view(), name="home"),
    path('check/', Checker, name="check"),
    path('usuarios/', ListaUsuarios.as_view(),name="user"),
    path('entradas/', Entradas.as_view(),name="ticket"),
    path('entradas/<pk>/', ConsultarEntrada.as_view(),name="consultar_entrada"),
    path('entradas_vendidas/', ListaEntradasVendidas.as_view(),name="entradas_vendidas"),
    path('procesar/', ProcesarEntrada.as_view(),name="process"),
    path('procesar/<pk>', EntradaProcesada.as_view(),name="entrada_procesada"),
    path('eventos/', AdminEventos.as_view(), name="admin"),
    path('perfil/', MiPerfil.as_view(),name="perfil"),
    path('registrar/', Registro.as_view(), name="signUp"),
    path('registrar/exito/', TemplateView.as_view(template_name='exito_registro.html'),name="exito"),
    path('ajax/crearevento/', CrearEvento),
    path('ajax/login/', Login),
    path('ajax/redirectSU/', RedirectSignUp),
    path('ajax/comprar_entrada/', ComprarEntrada),
    path('logout/', LogoutView.as_view(), name='logout')
]
