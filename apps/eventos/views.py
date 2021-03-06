from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Evento, Usuario, Organizacion, Usuario_Organizacion, Entrada, Medio_Pago, Pago, Registro_Participacion, Asiento
import uuid
from django.http import JsonResponse
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy, reverse
from .forms import *
import random
from pyzbar.pyzbar import decode
from PIL import Image
from django.forms.forms import NON_FIELD_ERRORS
import string

# CHECKER PARA REDIRIGIR AL INICIO ADECUADO


def Checker(request):
    if request.user.tipo_user.id == 1:
        return redirect('/entradas_vendidas/')
    elif request.user.tipo_user.id == 2:
        return redirect('/procesar/')
    else:
        return redirect('/')

# VISTAS GENÉRICAS DE DJANGO


class ListaEventos(ListView):
    model = Evento
    template_name = "inicio.html"

    def get_context_data(self, **kwargs):
        context = super(ListaEventos, self).get_context_data(**kwargs)
        context['object_list'] = Evento.objects.filter(
            estatus='V').order_by('fecha')
        return context


class AdminEventos(ListView):
    model = Evento
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = super(AdminEventos, self).get_context_data(**kwargs)
        context['object_list'] = Evento.objects.filter(
            estatus='V').order_by('fecha')
        return context


class Registro(CreateView):
    model = Usuario
    template_name = "registrar.html"
    form_class = CrearUsuario
    success_url = reverse_lazy('exito')

    def get_context_data(self, **kwargs):
        context = super(Registro, self).get_context_data(**kwargs)
        try:
            context['email'] = self.request.COOKIES['email']
            context['username'] = self.request.COOKIES['user']
        except:
            pass
        context['organizaciones'] = Organizacion.objects.filter(estatus='A')
        return context

    def form_valid(self, form):
        user = form.save()
        user_organizacion = Usuario_Organizacion()
        user_organizacion.puesto = form.cleaned_data['puesto']
        user_organizacion.organizacion = Organizacion.objects.get(
            id=form.cleaned_data['organizacion'])
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
        context['object_list'] = Entrada.objects.filter(
            usuario=self.request.user.id)
        return context


class ConsultarEntrada(DetailView):
    model = Entrada
    template_name = "consultar_entrada.html"

    def get_context_data(self, **kwargs):
        context = super(ConsultarEntrada, self).get_context_data(**kwargs)
        context['asientos'] = Asiento.objects.filter(entrada=self.kwargs['pk'])
        return context

class MiPerfil(TemplateView):
    template_name = "perfil.html"

    def get_context_data(self, **kwargs):
        context = super(MiPerfil, self).get_context_data(**kwargs)
        user_org = Usuario_Organizacion.objects.get(usuario=self.request.user)
        context['organizacion'] = Organizacion.objects.get(
            id=user_org.organizacion.id)
        context['puesto'] = user_org.puesto
        return context


class ListaUsuarios(ListView):
    model = Usuario
    template_name = "usuarios.html"


class ListaEntradasVendidas(ListView):
    model = Entrada
    template_name = "entradas_vendidas.html"

class ProcesarEntrada(CreateView):
    model = Registro_Participacion
    template_name = "procesar.html"
    form_class = ProcesarEntrada
    success_url = reverse_lazy('entrada_procesada')
    codigo = None

    def form_valid(self, form):
        imagen = form.cleaned_data['qr']
        data = decode(Image.open(imagen))
        if len(data) != 0:
            self.codigo = str(data[0].data)[2:-1]
            entrada = Entrada.objects.get(id=self.codigo)
            if entrada:
                if entrada.estatus == 'A':
                    reg = form.save(commit=False)
                    reg.encargado = self.request.user
                    reg.entrada = entrada
                    reg.save()
                    entrada.estatus = 'F'
                    entrada.save()
                    return super().form_valid(form)
                else:
                    form._errors[NON_FIELD_ERRORS] = form.error_class(['La entrada ya fue utilizada previamente.'])
                    return super().form_invalid(form)
            else:
                form._errors[NON_FIELD_ERRORS] = form.error_class(['La imagen no contiene un código QR válido.'])
                return super().form_invalid(form)
        else:
            form._errors[NON_FIELD_ERRORS] = form.error_class(['La imagen no contiene un código QR válido.'])
            return super().form_invalid(form)
        return super().form_valid(form)    

    def get_success_url(self):
        return reverse_lazy('entrada_procesada', kwargs={'pk': self.codigo})

class EntradaProcesada(DetailView):
    model = Entrada
    template_name = "entrada_procesada.html"

    def get_context_data(self, **kwargs):
        context = super(EntradaProcesada, self).get_context_data(**kwargs)
        context['asientos'] = Asiento.objects.filter(entrada=self.kwargs['pk'])
        return context

# AJAX

def CrearEvento(request):
    try:
        e = Evento()
        e.nombre = request.POST.get('nombre', None)
        e.fecha = request.POST.get('fecha', None)
        e.hora = request.POST.get('hora', None)
        e.lugar = request.POST.get('lugar', None)
        e.aforo = request.POST.get('aforo', None)
        e.precio = request.POST.get('precio', None)
        e.descripcion = request.POST.get('descripcion', None)
        e.save()
        return JsonResponse({'exito': True})
    except:
        return JsonResponse({'exito': False})


def Login(request):
    try:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'exito': True})
        else:
            return JsonResponse({'exito': False})
    except:
        return JsonResponse({'exito': False})


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
            response = JsonResponse({'exito': True})
            response.set_cookie('user', username, max_age=20)
            response.set_cookie('email', email, max_age=20)
            return response
        elif user_username != None and user_email == None:
            return JsonResponse({'exito': False, 'mensaje': 'Ya existe un usuario con ese nombre de usuario.'})
        elif user_username == None and user_email != None:
            return JsonResponse({'exito': False, 'mensaje': 'Ya existe un usuario con ese email.'})
        else:
            return JsonResponse({'exito': False, 'mensaje': 'Ya existe un usuario con ese nombre de usuario y ese email.'})
    except:
        return JsonResponse({'exito': False})


def ComprarEntrada(request):
    usuario = request.user
    id_evento = request.POST.get('evento', None)
    cantidad = request.POST.get('cantidad', None)
    evento = Evento.objects.get(id=id_evento)
    if int(evento.EntradasDisponibles()) < int(cantidad):
        return JsonResponse({'exito': False, 'mensaje': 'No hay suficientes entradas. Sólo hay ' + str(evento.EntradasDisponibles) + ' entradas disponibles.'})
    pago = Pago()
    pago.referencia = uuid.uuid4().hex[:8]
    medios = Medio_Pago.objects.filter(estatus='A')
    pago.medio_pago = random.choice(medios)
    pago.save()
    entrada = Entrada()
    entrada.costo = evento.precio
    entrada.cantidad = cantidad
    entrada.evento = evento
    entrada.forma_pago = pago
    entrada.usuario = usuario
    entrada.save()
    for i in range(0,int(cantidad)):
        asiento = Asiento()
        asiento.entrada = entrada
        asiento.fila = random.choice(string.ascii_letters)
        asiento.numero = random.randint(1,25)
        asiento.save()
    return JsonResponse({'exito': True, 'id': str(entrada.id)})
    # except:
    #     return JsonResponse({'exito': False, 'mensaje': 'Error desconocido del servidor.'})
