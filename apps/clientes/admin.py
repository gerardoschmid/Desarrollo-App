from django.contrib import admin
from .models import Cliente
from django.utils.translation import gettext_lazy as _
# from apps.reservas.models import Reserva # Para inlines si se desea

# class ReservaInlineForCliente(admin.TabularInline): # O StackedInline
#     model = Reserva
#     extra = 0 # No mostrar formularios vacíos por defecto
#     fields = ('habitacion', 'fecha_entrada', 'fecha_salida', 'estado', 'costo_total')
#     readonly_fields = ('habitacion', 'fecha_entrada', 'fecha_salida', 'estado', 'costo_total') # Hacerlos de solo lectura en el inline
#     can_delete = False # No permitir borrar reservas desde el perfil del cliente directamente
#     show_change_link = True # Permitir ir al detalle de la reserva

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'get_cantidad_reservas', 'created_at')
    search_fields = ('nombre', 'apellidos', 'email', 'telefono')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    # inlines = [ReservaInlineForCliente] # Descomentar si se define el inline

    fieldsets = (
        (_('Información Personal'), {
            'fields': ('nombre', 'apellidos')
        }),
        (_('Información de Contacto'), {
            'fields': ('email', 'telefono')
        }),
        # (_('Asociación con Usuario del Sistema'), { # Si se usa el campo user
        #     'fields': ('user',)
        # }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def get_cantidad_reservas(self, obj):
        # Contar las reservas asociadas a este cliente
        return obj.reserva_set.count() # Asume related_name por defecto 'reserva_set'
    get_cantidad_reservas.short_description = _('Nº de Reservas')
