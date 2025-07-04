# Contenido de clientes/admin.py
from django.contrib import admin
from django.db.models import Count # Para anotar el número de reservas
from django.urls import reverse
from django.utils.html import format_html

from .models import Cliente
from reservas.models import Reserva # Para el inline o para contar reservas

class ReservaInlineForCliente(admin.TabularInline):
    model = Reserva
    fields = ('codigo_reserva_link', 'tipo_habitacion_solicitada', 'fecha_llegada', 'fecha_salida', 'estado', 'precio_total_formateado')
    readonly_fields = fields # Todos los campos son solo de lectura en este inline
    extra = 0
    can_delete = False
    show_change_link = False # No mostrar link de cambio para la reserva desde aquí, usar el link en codigo_reserva_link
    verbose_name = "Reserva Asociada"
    verbose_name_plural = "Historial de Reservas de Este Cliente"
    ordering = ['-fecha_llegada']
    max_num = 10 # Mostrar máximo 10 reservas recientes, o quitar para todas

    def codigo_reserva_link(self, obj):
        if obj.pk: # Asegurarse que el objeto Reserva exista
            url = reverse("admin:reservas_reserva_change", args=[obj.pk])
            return format_html('<a href="{}"><strong>{}</strong></a>', url, obj.codigo_reserva)
        return "N/A (Reserva no guardada)"
    codigo_reserva_link.short_description = "Código Reserva"

    def precio_total_formateado(self, obj):
        return f"${obj.precio_total:,.2f}" if obj.precio_total is not None else "N/A"
    precio_total_formateado.short_description = "Precio Total"

    def has_add_permission(self, request, obj=None):
        # No permitir añadir reservas directamente desde el perfil del cliente en el admin
        return False

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'telefono', 'fecha_registro_corta', 'cantidad_reservas_realizadas')
    search_fields = ('nombre_completo__icontains', 'email__icontains', 'telefono__icontains')
    list_filter = ('fecha_registro', 'pais_residencia') # Asumiendo que añades 'pais_residencia'
    readonly_fields = ('fecha_registro', 'ultima_actualizacion', 'cantidad_reservas_realizadas_display')
    inlines = [ReservaInlineForCliente]
    date_hierarchy = 'fecha_registro'
    list_per_page = 25

    fieldsets = (
        ("Información Personal", {
            'fields': ('nombre_completo', 'email', 'telefono')
        }),
        ("Detalles Adicionales", {
            'fields': ('tipo_documento', 'numero_documento', 'fecha_nacimiento', 'pais_residencia', 'direccion_completa'),
            'classes': ('collapse',), # Ocultar por defecto
        }),
        ("Notas Internas", {
            'fields': ('notas_internas',),
            'classes': ('collapse',)
        }),
        ("Auditoría y Resumen", {
            'fields': ('fecha_registro', 'ultima_actualizacion', 'cantidad_reservas_realizadas_display'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        # Anotar el conteo de reservas para poder ordenarlo y mostrarlo eficientemente
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _cantidad_reservas=Count('reservas_cliente') # Usar el related_name del modelo Reserva
        )
        return queryset

    def cantidad_reservas_realizadas(self, obj):
        return obj._cantidad_reservas # Usar el valor anotado
    cantidad_reservas_realizadas.short_description = "Nº Reservas"
    cantidad_reservas_realizadas.admin_order_field = '_cantidad_reservas' # Permitir ordenar por esta columna

    def cantidad_reservas_realizadas_display(self, obj):
        # Para mostrar en readonly_fields, ya que no puede ser el método directo con parámetros
        return obj._cantidad_reservas
    cantidad_reservas_realizadas_display.short_description = "Número Total de Reservas Realizadas"

    def fecha_registro_corta(self, obj):
        return obj.fecha_registro.strftime("%d/%m/%Y")
    fecha_registro_corta.short_description = "Fecha Registro"
    fecha_registro_corta.admin_order_field = "fecha_registro"
```
