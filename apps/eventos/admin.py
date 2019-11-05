from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Tipo_Usuario)
admin.site.register(Usuario)
admin.site.register(Medio_Pago)
admin.site.register(Organizacion)
admin.site.register(Usuario_Organizacion)
admin.site.register(Evento)
admin.site.register(Pago)
admin.site.register(Entrada)
admin.site.register(Registro_Participacion)