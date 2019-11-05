from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Evento, Usuario
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.forms import Form

## VISTAS GENÉRICAS DE DJANGO


class CrearUsuario(TemplateView):
    template_name = "registrar.html"
    
class ListaEventos(ListView):
    model = Evento
    template_name = "inicio.html"

    def get_context_data(self, **kwargs):
        context = super(ListaEventos, self).get_context_data(**kwargs)
        context['object_list'] = Evento.objects.filter(estatus='V').order_by('fecha')
        return context

class AdminEventos(ListView):
    model = Evento
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminEventos, self).get_context_data(**kwargs)
        context['object_list'] = Evento.objects.filter(estatus='V').order_by('fecha')
        return context

### AJAX

def CrearEvento(request):
    try:
        e = Evento()
        e.nombre = request.POST.get('nombre',None)
        e.fecha = request.POST.get('fecha',None)
        e.hora = request.POST.get('hora',None)
        e.lugar = request.POST.get('lugar',None)
        e.aforo = request.POST.get('aforo',None)
        e.precio = request.POST.get('precio',None)
        e.descripcion = request.POST.get('descripcion',None)
        e.save()
        return JsonResponse({'exito':True})
    except:
        return JsonResponse({'exito':False})

def Login(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'exito':True})
        else:
            return JsonResponse({'exito':False})
    except:
        return JsonResponse({'exito':False})


def RedirectSignUp(request):
    try:
        response = JsonResponse({'exito': True})
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        response.set_cookie('signUp-user', username)
        response.set_cookie('signUp-email', email)
        return response
    except:
        return JsonResponse({'exito': False})
