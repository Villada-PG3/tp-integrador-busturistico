from django import forms
from .models import *
from datetime import date
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}))
    password = forms.CharField(label="Contraseña (Legajo)", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

class RecorridoForm(forms.ModelForm):
    class Meta:
        model = Recorrido
        fields = ['nombre', 'frecuencia', 'hora_inicio', 'hora_fin']
class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ('chofer', 'bus', 'recorrido', 'horario_inicio_programado', 'horario_fin_programado', 'fecha_viaje')
        
        widgets = {
            'fecha_viaje': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ViajeForm, self).__init__(*args, **kwargs)
        # Filtrar los buses habilitados
        self.fields['bus'].queryset = Bus.objects.filter(estado_bus__nombre='Habilitado')
    def clean_fecha_viaje(self):
        fecha_viaje = self.cleaned_data.get('fecha_viaje')
        if fecha_viaje < date.today():
            raise forms.ValidationError("La fecha de viaje no puede ser anterior a la fecha actual.")
        return fecha_viaje
        
        
class BusForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['patente', 'num_unidad', 'fecha_compra', 'estado_bus']
        widgets = {
            'patente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la patente'}),
            'num_unidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el número de unidad'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_bus': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean_num_unidad(self):
        num_unidad = self.cleaned_data.get('num_unidad')
        if num_unidad <= 0:
            raise forms.ValidationError("El número de unidad debe ser positivo.")
        return num_unidad
    def clean_fecha_compra(self):
        fecha_compra = self.cleaned_data.get('fecha_compra')
        if fecha_compra > date.today():
            raise forms.ValidationError("La fecha de compra no puede ser posterior a la fecha actual.")
        return fecha_compra
