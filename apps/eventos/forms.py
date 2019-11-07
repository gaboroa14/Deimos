from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Registro_Participacion

class BaseCrearUsuario(UserCreationForm):

    class Meta:
        model = Usuario

        fields = [
            'username',
            'nombre',
            'correo',
            'sexo',
            'fecha_nacimiento',
            'password1',
            'password2',
        ]

class CrearUsuario(BaseCrearUsuario):
    organizacion = forms.CharField()
    puesto = forms.CharField()

    class Meta(BaseCrearUsuario.Meta):
        fields = BaseCrearUsuario.Meta.fields + ['organizacion','puesto']

class ProcesarEntrada(forms.ModelForm):

    class Meta:
        model = Registro_Participacion

        fields = [
            'qr'
        ]