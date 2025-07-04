# Contenido de reservas/admin.py
from django.contrib import admin
from .models import Reserva, HuespedAdicional
from django.utils.html import format_html
from django.urls import reverse
from django.utils.http import urlencode

class HuespedAdicionalInline(admin.TabularInline):
    model = HuespedAdicional
    extra = 0 # No mostrar formularios vacíos por defecto
    fields = ('nombre_completo', 'edad', 'documento_identidad')
    verbose_name = "Huésped Adicional"
    verbose_name_plural = "Otros Huéspedes Registrados en esta Reserva"
    # min_num = 0 # Permitir cero huéspedes adicionales

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo_reserva_link', 'cliente_link', 'tipo_habitacion_solicitada',
        'fecha_llegada', 'fecha_salida', 'noches_estadia_display', 'numero_total_huespedes',
        'estado_display', 'precio_total_formateado', 'habitacion_asignada_link', 'fecha_creacion_corta'
    )
    list_filter = ('estado', 'fecha_llegada', 'tipo_habitacion_solicitada__nombre', 'fecha_creacion')
    search_fields = (
        'codigo_reserva__iexact', # Búsqueda exacta para UUID
        'cliente__nombre_completo__icontains',
        'cliente__email__icontains',
        'tipo_habitacion_solicitada__nombre__icontains',
        'habitacion_asignada__numero__iexact'
    )
    readonly_fields = ('codigo_reserva', 'fecha_creacion', 'fecha_actualizacion', 'precio_total')
    autocomplete_fields = ['cliente', 'tipo_habitacion_solicitada', 'habitacion_asignada']
    inlines = [HuespedAdicionalInline]
    date_hierarchy = 'fecha_llegada' # Navegación por fechas de llegada
    list_per_page = 20
    ordering = ('-fecha_llegada', '-fecha_creacion')

    fieldsets = (
        ("Información Principal de la Reserva", {
            'fields': ('codigo_reserva', 'cliente', 'estado')
        }),
        ("Detalles de Estancia Solicitada", {
            'fields': ('tipo_habitacion_solicitada', 'fecha_llegada', 'fecha_salida',
                       'numero_huespedes_adultos', 'numero_huespedes_ninos')
        }),
        ("Asignación y Costos", {
            'fields': ('habitacion_asignada', 'precio_total') # precio_total es readonly, calculado
        }),
        ("Notas", {
            'fields': ('notas_adicionales_cliente', 'notas_internas_hotel'),
            'classes': ('collapse',) # Ocultar por defecto
        }),
        ("Auditoría", {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

    def codigo_reserva_link(self, obj):
        url = reverse("admin:reservas_reserva_change", args=[obj.pk])
        return format_html('<a href="{}"><strong>{}</strong></a>', url, obj.codigo_reserva)
    codigo_reserva_link.short_description = "Código Reserva"
    codigo_reserva_link.admin_order_field = 'codigo_reserva'

    def cliente_link(self, obj):
        if obj.cliente:
            url = reverse("admin:clientes_cliente_change", args=[obj.cliente.pk])
            return format_html('<a href="{}">{}</a>', url, obj.cliente.nombre_completo)
        return "N/A"
    cliente_link.short_description = "Cliente"
    cliente_link.admin_order_field = 'cliente__nombre_completo'

    def habitacion_asignada_link(self, obj):
        if obj.habitacion_asignada:
            url = reverse("admin:habitaciones_habitacion_change", args=[obj.habitacion_asignada.pk])
            return format_html('<a href="{}">{} ({})</a>', url, obj.habitacion_asignada.numero, obj.habitacion_asignada.tipo_habitacion.nombre)
        return "Sin asignar"
    habitacion_asignada_link.short_description = "Hab. Asignada"
    habitacion_asignada_link.admin_order_field = 'habitacion_asignada__numero'

    def precio_total_formateado(self, obj):
        return f"${obj.precio_total:,.2f}" if obj.precio_total is not None else "N/A"
    precio_total_formateado.short_description = "Precio Total"
    precio_total_formateado.admin_order_field = 'precio_total'

    def noches_estadia_display(self, obj):
        return obj.noches_estadia
    noches_estadia_display.short_description = "Noches"
    # No se puede ordenar directamente por property, requeriría anotación en queryset

    def estado_display(self, obj):
        # Para mostrar colores o iconos según el estado
        estado_map = {
            'pendiente': ('fas fa-clock text-warning', 'Pendiente'),
            'confirmada': ('fas fa-check-circle text-success', 'Confirmada'),
            'cancelada': ('fas fa-times-circle text-danger', 'Cancelada'),
            'completada': ('fas fa-flag-checkered text-info', 'Completada'),
            'no_show': ('fas fa-user-slash text-muted', 'No Show'),
        }
        icon_class, text_display = estado_map.get(obj.estado, ('fas fa-question-circle', obj.get_estado_display()))
        return format_html('<i class="{} me-1"></i>{}', icon_class, text_display)
    estado_display.short_description = "Estado"
    estado_display.admin_order_field = 'estado'

    def fecha_creacion_corta(self,obj):
        return obj.fecha_creacion.strftime("%d/%m/%y %H:%M")
    fecha_creacion_corta.short_description = "Fecha Creación"
    fecha_creacion_corta.admin_order_field = 'fecha_creacion'


    def get_queryset(self, request):
        # Optimizar consultas
        return super().get_queryset(request).select_related(
            'cliente',
            'tipo_habitacion_solicitada',
            'habitacion_asignada',
            'habitacion_asignada__tipo_habitacion' # Para el link de habitación asignada
        )

    # Acciones personalizadas
    def marcar_como_confirmada(self, request, queryset):
        updated_count = 0
        for reserva in queryset:
            if reserva.estado == 'pendiente': # Solo confirmar las pendientes
                reserva.estado = 'confirmada'
                # Aquí podrías añadir lógica para asignar habitación si no está asignada
                # o enviar email de confirmación
                reserva.save()
                updated_count += 1
        if updated_count > 0:
            self.message_user(request, f"{updated_count} reserva(s) han sido marcadas como confirmadas.")
        else:
            self.message_user(request, "No se actualizaron reservas (posiblemente no estaban en estado 'pendiente').", level='WARNING')
    marcar_como_confirmada.short_description = "Marcar seleccionadas como Confirmadas"

    def marcar_como_cancelada(self, request, queryset):
        # Considerar estados desde los que se puede cancelar
        updated_count = queryset.update(estado='cancelada')
        # Aquí podrías añadir lógica para liberar habitaciones asignadas
        self.message_user(request, f"{updated_count} reserva(s) han sido marcadas como canceladas.")
    marcar_como_cancelada.short_description = "Marcar seleccionadas como Canceladas"

    actions = [marcar_como_confirmada, marcar_como_cancelada]

    # Añadir FontAwesome al admin para los iconos de estado_display
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',)
        }

# No es necesario registrar HuespedAdicional aquí si solo se usa como inline.
# Si quieres gestionarlos independientemente:
# @admin.register(HuespedAdicional)
# class HuespedAdicionalAdmin(admin.ModelAdmin):
#     list_display = ('nombre_completo', 'reserva_link', 'edad')
#     search_fields = ('nombre_completo', 'reserva__codigo_reserva')
#     autocomplete_fields = ['reserva']

#     def reserva_link(self, obj):
#         if obj.reserva:
#             url = reverse("admin:reservas_reserva_change", args=[obj.reserva.pk])
#             return format_html('<a href="{}">{}</a>', url, obj.reserva.codigo_reserva)
#         return "N/A"
#     reserva_link.short_description = "Reserva Asociada"
```
