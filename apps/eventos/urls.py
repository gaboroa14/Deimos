from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='inicio.html'),name="home"),
    path('usuarios/', TemplateView.as_view(template_name='usuarios.html'),name="user"),
    path('entradas/', TemplateView.as_view(template_name='entradas.html'),name="ticket"),
    path('procesar/', TemplateView.as_view(template_name='procesar.html'),name="process"),
]