from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('', ListaEventos.as_view(), name="home"),
    path('usuarios/', TemplateView.as_view(template_name='usuarios.html'),name="user"),
    path('entradas/', TemplateView.as_view(template_name='entradas.html'),name="ticket"),
    path('procesar/', TemplateView.as_view(template_name='procesar.html'),name="process"),
    path('eventos/', AdminEventos.as_view(), name="admin"),
    path('registrar/', CrearUsuario.as_view(), name="signUp"),
    path('ajax/crearevento/', CrearEvento),
    path('ajax/login/', Login),
    path('ajax/redirectSU/', RedirectSignUp),
    path('logout/', LogoutView.as_view(), name='logout')
]
