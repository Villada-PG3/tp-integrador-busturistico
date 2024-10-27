from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, View,CreateView
import requests
from typing import Any
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import *
from .models import *
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.exceptions import ValidationError

# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    
class BaseView(TemplateView):
    template_name = 'base/base.html'
    
class RecorridoListView(ListView):
    model = Recorrido
    template_name = 'recorrido/recorridos.html'
    context_object_name = 'recorridos'
    
class ParadaDetailView(DetailView):
    model = Parada
    template_name = 'parada/parada.html'
    context_object_name = 'parada'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['atractivos'] = AtractivoXParada.objects.filter(parada=self.object).select_related('atractivo')
        return context
    
class RecorridoDetailView(DetailView):
    model = Recorrido
    template_name = 'recorrido/recorrido.html'
    context_object_name = 'recorrido'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las paradas asociadas a este recorrido
        context['paradas'] = OrdenParada.objects.filter(recorrido=self.object).select_related('parada').order_by('asignacion_paradas')
        return context
    
class NuevoRecorridoView(FormView):
    template_name = 'recorrido/nuevorecorrido.html'
    form_class = RecorridoForm
    success_url = reverse_lazy('recorrido')  

    def form_valid(self, form):
        form.save()  
        return super().form_valid(form)
    
    
class ChoferLoginView(LoginView):
    template_name = 'chofer/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        # Guarda el legajo (contraseña original) en la sesión antes de que se hashee
        legajo = form.cleaned_data['password']
        response = super().form_valid(form)
        self.request.session['legajo_chofer'] = legajo
        return response

    def get_success_url(self):
        return reverse_lazy('index')
    

class MarcarViajeView(LoginRequiredMixin, TemplateView):
    template_name = 'chofer/marcar_viaje.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Obtener el legajo de la sesión
            legajo = self.request.session.get('legajo_chofer')
            print(f"Legajo en sesión: {legajo}")
            
            chofer = Chofer.objects.get(legajo=legajo)
            print(f"Chofer encontrado: {chofer}") # Agregamos más información de depuración
            
            viajes_chofer = Viaje.objects.filter(chofer=chofer)
            print(f"Viajes del chofer: {viajes_chofer}")
            
            viaje = viajes_chofer.last()
            print(f"Último viaje encontrado: {viaje}")
            
            context['viaje'] = viaje
            
        except Chofer.DoesNotExist:
            print("ERROR: No se encontró el chofer")
            context['viaje'] = None
        except Exception as e:
            print(f"ERROR: {str(e)}")
            context['viaje'] = None
        
        return context

    def post(self, request, *args, **kwargs):
        try:
            legajo = request.session.get('legajo_chofer')
            chofer = Chofer.objects.get(legajo=legajo)
            viaje_id = request.POST.get('id')
            viaje = get_object_or_404(Viaje, id=viaje_id, chofer=chofer)
            action = request.POST.get('action')

            fecha_actual = timezone.now().date()
            if action == 'inicio' and not viaje.marca_inicio_viaje_real:
                if fecha_actual == viaje.fecha_viaje:
                    viaje.marca_inicio_viaje_real = timezone.now()
                    viaje.estado_viaje = EstadoViaje.objects.get(nombre='En Curso')  # Cambiar el estado a "En Curso"
                    viaje.save()
                else:
                    messages.error(request, "No puedes iniciar el viaje antes de la fecha programada.")
                return redirect('marcar_viaje')
            elif action == 'final':
                
                if viaje.marca_inicio_viaje_real:  # Verificar que el viaje haya comenzado
                    viaje.marca_fin_viaje_real = timezone.now()
                    viaje.estado_viaje = EstadoViaje.objects.get(nombre='Finalizado')
                    viaje.save()
                    messages.success(request, "Viaje finalizado correctamente.")
                else:
                    messages.error(request, "Debes iniciar el viaje antes de finalizarlo.")
                return redirect('marcar_viaje')

        except (Chofer.DoesNotExist, Viaje.DoesNotExist, EstadoViaje.DoesNotExist):
            pass

        return redirect('marcar_viaje')
    
    
class ViajeListView(ListView):
    model = Viaje
    template_name = 'viaje/viaje.html'
    context_object_name = 'viajes'

    def get_queryset(self):
        return Viaje.objects.all().select_related(
            'chofer', 
            'bus', 
            'recorrido', 
            'estado_viaje'
        ).order_by('-fecha_viaje')
        
    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:  # Para eliminar un viaje
            viaje_id = request.POST.get('viaje_id')
            viaje = get_object_or_404(Viaje, id=viaje_id)  # Cambiado de Bus a Viaje
            viaje.delete()
            return HttpResponseRedirect(request.path)
        
class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'viaje/viaje_detalle.html'
    context_object_name = 'viaje'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viaje = self.object
        # Aquí puedes agregar más contexto si lo necesitas
        return context
    
class CrearViajeView(FormView):
    template_name = 'viaje/crear_viaje.html'
    form_class = ViajeForm
    success_url = reverse_lazy('viajes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtra los buses que están habilitados
        context['buses_habilitados'] = Bus.objects.filter(estado_bus__nombre='Habilitado')  
        return context

    def form_valid(self, form):
        viaje = form.save(commit=False)  # No guardamos aún en la base de datos
        viaje.estado_viaje = EstadoViaje.objects.get(nombre='Por Empezar')  # Establecer el estado predeterminado
        viaje.save()  # Ahora guardamos el viaje
        return super().form_valid(form)

class EditarViajeView(UpdateView):
    model = Viaje
    template_name = 'viaje/editar_viaje.html'
    form_class = ViajeForm
    success_url = reverse_lazy('viajes')


    
class BusListView(ListView):
    model = Bus
    template_name = 'bus/buses.html'  # Nombre del template que mostraría la lista de buses
    context_object_name = 'buses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados'] = EstadoBus.objects.all()  # Pasar los estados de bus al template
        return context

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:  # Para eliminar un bus
            bus_id = request.POST.get('bus_id')
            bus = get_object_or_404(Bus, id=bus_id)
            bus.delete()
            return HttpResponseRedirect(request.path)  # Redirigir a la misma página después de eliminar

        if 'change_status' in request.POST:  # Para cambiar el estado del bus
            bus_id = request.POST.get('bus_id')
            estado_bus_id = request.POST.get('estado_bus')
            bus = get_object_or_404(Bus, id=bus_id)
            estado_bus = EstadoBus.objects.get(id=estado_bus_id)
            bus.estado_bus = estado_bus
            bus.save()
            return HttpResponseRedirect(request.path)
        
class CrearBusView(CreateView):
    model = Bus
    form_class = BusForm
    template_name = 'bus/crear_bus.html'
    success_url = reverse_lazy('buses')

    def form_valid(self, form):
        messages.success(self.request, 'Bus creado con éxito')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Aquí puedes agregar un mensaje de error si lo deseas
        messages.error(self.request, 'Por favor corrige los errores en el formulario.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class BusController:
    @staticmethod
    def crear_bus(data):
        print("Datos recibidos para crear bus:", data)
        # Validar si la patente es válida
        patente = data.get('patente')
        if Bus.objects.filter(patente=patente).exists():
            raise ValueError('La patente ya existe.')

        # Validar si el número de unidad es válido
        num_unidad = data.get('num_unidad')
        if Bus.objects.filter(num_unidad=num_unidad).exists():
            raise ValueError('El número de unidad ya existe.')

        # Validar si el estado del bus es 'Habilitado'
        estado_bus = data.get('estado_bus')
        if estado_bus is None or estado_bus.nombre != 'Habilitado':
            raise ValueError('El bus debe estar habilitado.')

        # Crear y guardar el bus
        bus = Bus(**data)
        bus.save()
        return bus

    @staticmethod
    def obtener_bus(bus_id):
        return Bus.objects.get(id=bus_id)

    @staticmethod
    def eliminar_bus(bus_id):
        bus = Bus.objects.get(id=bus_id)
        bus.delete()
        
        
    
class ViajeController:
    @staticmethod
    def crear_viaje(data):
        viaje = Viaje(**data)
        viaje.save()
        return viaje

    @staticmethod
    def obtener_viaje(viaje_id):
        return Viaje.objects.get(id=viaje_id)

    @staticmethod
    def eliminar_viaje(viaje_id):
        viaje = Viaje.objects.get(id=viaje_id)
        viaje.delete()



class ChoferController:
    @staticmethod
    def crear_chofer(data):
        chofer = Chofer(**data)
        chofer.save()
        return chofer

    @staticmethod
    def obtener_chofer(chofer_id):
        return Chofer.objects.get(id=chofer_id)

    @staticmethod
    def eliminar_chofer(chofer_id):
        chofer = Chofer.objects.get(id=chofer_id)
        chofer.delete()
    

