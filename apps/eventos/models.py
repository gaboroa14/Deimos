from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
import qrcode

# Create your models here.

ESTATUS = (
    ('A','Activo'),
    ('I','Inactivo')
)

class Tipo_Usuario (models.Model):
    nombre = models.CharField(max_length=20)
    estatus = models.CharField(max_length=1, choices=ESTATUS, default='A')

class Usuario (AbstractUser):
    nombre = models.CharField(max_length=25,null=True,blank=True)
    apellido = models.CharField(max_length=25,null=True,blank=True)
    tipo_user = models.ForeignKey(Tipo_Usuario,on_delete=models.CASCADE,null=True,blank=True)
    SEXO = (
        ('M','Masculino'),
        ('F','Femenino')
    )
    sexo = models.CharField(max_length=1,choices=SEXO,null=True,blank=True)
    fecha_nacimiento = models.DateField(null=True,blank=True)
    correo = models.EmailField(null=True,blank=True)
    estatus = models.CharField(max_length=1,choices=ESTATUS, default='A')

class Medio_Pago(models.Model):
    nombre = models.CharField(max_length=50)
    TIPOS = (
        ('D','Divisa'),
        ('N','Nacional')
    )
    tipo = models.CharField(max_length=1,choices=TIPOS)
    estatus = models.CharField(max_length=1,choices=ESTATUS, default='A')

class Organizacion(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    ubicacion = models.CharField(max_length=50)
    estatus = models.CharField(max_length=1,choices=ESTATUS, default='A')

class Usuario_Organizacion(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    organizacion = models.ForeignKey(Organizacion,on_delete=models.CASCADE)
    puesto = models.CharField(max_length=50)

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    lugar = models.CharField(max_length=25)
    aforo = models.IntegerField()
    precio = models.FloatField()
    descripcion = models.CharField(max_length=500)
    ESTATUS_EVENTO = (
        ('P','Preventa'),
        ('V','Venta'),
        ('F','Finalizado'),
        ('C','Cancelado')
    )
    estatus = models.CharField(max_length=1,choices=ESTATUS_EVENTO, default='V')

class Pago(models.Model):
    medio_pago = models.ForeignKey(Medio_Pago,models.CASCADE)
    referencia = models.CharField(max_length=25)
    comprobante = models.ImageField(upload_to='comprobantes/')
    ESTATUS_PAGO = (
        ('P','Pendiente de aprobación'),
        ('A','Aprobado')
    )
    estatus = models.CharField(max_length=1,choices=ESTATUS_PAGO,default='A')

class Entrada(models.Model):
    id = models.CharField(max_length=100,primary_key=True,default=uuid.uuid4)
    evento = models.ForeignKey(Evento, models.CASCADE)
    usuario = models.ForeignKey(Usuario, models.CASCADE)
    forma_pago = models.ForeignKey(Pago, models.CASCADE)
    fecha = models.DateField(auto_now=True)
    costo = models.FloatField()
    cantidad = models.IntegerField()
    qr = models.ImageField(upload_to='media/qr/', blank=True, null=True)
    ESTATUS_ENTRADA = (
        ('P','Pendiente por aprobación'),
        ('A','Aprobada'),
        ('F','Utilizada')
    )
    estatus = models.CharField(max_length=1,choices=ESTATUS_ENTRADA,default='A')

class Registro_Participacion(models.Model):
    entrada = models.ForeignKey(Entrada,models.CASCADE)
    encargado = models.ForeignKey(Usuario,models.CASCADE)
    fecha = models.DateField(auto_now=True)
    estatus = models.CharField(max_length=1,choices=ESTATUS)

@receiver(post_save,sender=Entrada)
def ImagenQR(sender, instance, **kwargs):
    if instance.qr == None:
        img = qrcode.make(instance.id)
        with open('/home/gabriel/Deimos/media/qr/' + instance.id + '.png', 'wb') as f:
            img.save(f)
        instance.qr = 'qr/' + instance.id + '.png'
        instance.save()