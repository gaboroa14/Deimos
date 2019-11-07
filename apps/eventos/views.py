from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Evento, Usuario, Organizacion, Usuario_Organizacion, Entrada
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import *

## VISTAS GENÉRICAS DE DJANGO
    
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

class Registro(CreateView):
    model = Usuario
    template_name = "registrar.html"
    form_class = CrearUsuario
    success_url = reverse_lazy('exito')

    def get_context_data(self, **kwargs):
        context = super(Registro, self).get_context_data(**kwargs)
        try:
            context['email'] = self.request.GET['email']
            context['username'] = self.request.GET['username']
        except:
            pass
        context['organizaciones'] = Organizacion.objects.filter(estatus='A')
        return context
    
    def form_valid(self, form):
        user = form.save()
        user_organizacion = Usuario_Organizacion()
        user_organizacion.puesto = form.cleaned_data['puesto']
        user_organizacion.organizacion = Organizacion.objects.get(id=form.cleaned_data['organizacion'])
        user_organizacion.usuario = user
        user_organizacion.save()
        nombres = user.nombre.split(maxsplit=2)
        if len(nombres) > 1:
            user.nombre = nombres[0]
            user.apellido = nombres[1]
            user.save()
        else:
            user.apellido = ""
            user.save()
        return super().form_valid(form)

class Entradas(ListView):
    model = Entrada
    template_name = "entradas.html"

    def get_context_data(self, **kwargs):
        context = super(Entradas, self).get_context_data(**kwargs)
        print(self.request.user.id)
        context['object_list'] = Entrada.objects.filter(usuario=self.request.user.id)
        print(context['object_list'])
        return context

class ConsultarEntrada(DetailView):
    model = Entrada
    template_name = "consultar_entrada.html"

class MiPerfil(TemplateView):
    template_name = "perfil.html"

    def get_context_data(self, **kwargs):
        context = super(MiPerfil, self).get_context_data(**kwargs)
        user_org = Usuario_Organizacion.objects.get(usuario=self.request.user)
        context['organizacion'] = Organizacion.objects.get(id=user_org.organizacion.id)
        context['puesto'] = user_org.puesto
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
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        try:
            user_username = Usuario.objects.get(username=username)
        except:
            user_username = None
        try:
            user_email = Usuario.objects.get(correo=email)
        except:
            user_email = None
        if user_username == None and user_email == None:
            return JsonResponse({'exito': True})
        elif user_username != None and user_email == None:
            return JsonResponse({'exito': False,'mensaje':'Ya existe un usuario con ese nombre de usuario.'})
        elif user_username == None and user_email != None:
            return JsonResponse({'exito': False,'mensaje':'Ya existe un usuario con ese email.'})
        else:
            return JsonResponse({'exito': False,'mensaje':'Ya existe un usuario con ese nombre de usuario y ese email.'})
    except:
        return JsonResponse({'exito': False})