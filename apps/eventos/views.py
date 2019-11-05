from django.shortcuts import render
from .models import Evento
from django.http import JsonResponse
from django.views.generic.list import ListView

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