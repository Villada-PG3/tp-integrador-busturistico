from django.contrib import admin
from .models import EstadoBus, EstadoViaje, Recorrido, Parada, TipoParada, Atractivo, AtractivoXParada, OrdenParada, Bus, Chofer, Viaje
from django.contrib.auth.models import User


class BusAdmin(admin.ModelAdmin):
    search_fields = ('patente', 'num_unidad')  
    list_display = ('patente', 'num_unidad', 'fecha_compra')  
    list_filter = ('estado_bus',) 


class ChoferAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'nombre', 'apellido']  

    def save_model(self, request, obj, form, change):
        username = obj.nombre +' '+  obj.apellido
        password = str(obj.legajo)  
        name = obj.nombre
        lastname = obj.apellido
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
        user.first_name = name
        user.last_name = lastname
        user.is_staff = True
        user.save()
        super().save_model(request, obj, form, change)


class ViajeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chofer', 'bus', 'recorrido', 'estado_viaje', 'fecha_viaje')  
    list_filter = ('estado_viaje', 'fecha_viaje')  
    search_fields = ('chofer__nombre', 'bus__num_unidad', 'recorrido__nombre')  


class OrdenParadaAdmin(admin.ModelAdmin):
    list_display = ('parada', 'recorrido', 'asignacion_paradas')
    list_filter = ('recorrido',)
    search_fields = ('parada__nombre', 'recorrido__nombre')


admin.site.register(EstadoBus)
admin.site.register(EstadoViaje)
admin.site.register(Recorrido)
admin.site.register(Parada)
admin.site.register(TipoParada)
admin.site.register(Atractivo)
admin.site.register(AtractivoXParada)
admin.site.register(OrdenParada, OrdenParadaAdmin)  # Aquí registramos el admin personalizado


admin.site.register(Bus, BusAdmin)
admin.site.register(Chofer, ChoferAdmin)
admin.site.register(Viaje, ViajeAdmin)