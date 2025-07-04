from django.contrib import admin
from .models import Reserva
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'id',
        'cliente_link',
        'habitacion_link',
        'fecha_entrada',
        'fecha_salida',
        'numero_huespedes', # Añadido
        'estado_formateado',
        'costo_total',
        'created_at'
    )
    list_filter = ('estado', 'fecha_entrada', 'fecha_salida', 'habitacion__tipo_habitacion', 'numero_huespedes', 'created_at') # Añadido numero_huespedes
    search_fields = ('id', 'cliente__nombre', 'cliente__apellidos', 'cliente__email', 'habitacion__numero_habitacion', 'numero_huespedes') # Añadido numero_huespedes
    list_editable = () # 'estado' podría ser editable si se desea con cuidado
    readonly_fields = ('created_at', 'updated_at', 'costo_total_calculado') # costo_total podría ser calculado o manual
    date_hierarchy = 'fecha_entrada'

    fieldsets = (
        (_('Información Principal'), {
            'fields': ('cliente', 'habitacion')
        }),
        (_('Fechas y Huéspedes'), {
            'fields': ('fecha_entrada', 'fecha_salida', 'numero_huespedes')
        }),
        (_('Estado y Costo'), {
            'fields': ('estado', 'costo_total', 'costo_total_calculado') # Mostrar el calculado como readonly
        }),
        (_('Adicional'), {
            'fields': ('notas_adicionales',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    raw_id_fields = ('cliente', 'habitacion') # Útil si hay muchos clientes/habitaciones

    def get_queryset(self, request):
        # Optimizar queryset para incluir datos relacionados
        return super().get_queryset(request).select_related('cliente', 'habitacion', 'habitacion__tipo_habitacion')

    def cliente_link(self, obj):
        from django.urls import reverse
        if obj.cliente:
            link = reverse("admin:clientes_cliente_change", args=[obj.cliente.id])
            return format_html('<a href="{}">{}</a>', link, obj.cliente.nombre_completo)
        return "-"
    cliente_link.short_description = _('Cliente')
    cliente_link.admin_order_field = 'cliente'

    def habitacion_link(self, obj):
        from django.urls import reverse
        if obj.habitacion:
            link = reverse("admin:habitaciones_habitacion_change", args=[obj.habitacion.id])
            return format_html('<a href="{}">{} ({})</a>', link, obj.habitacion.numero_habitacion, obj.habitacion.tipo_habitacion.nombre)
        return "-"
    habitacion_link.short_description = _('Habitación')
    habitacion_link.admin_order_field = 'habitacion'

    def estado_formateado(self, obj):
        if obj.estado == Reserva.ESTADO_CONFIRMADA:
            color = "green"
        elif obj.estado == Reserva.ESTADO_PENDIENTE:
            color = "orange"
        elif obj.estado == Reserva.ESTADO_CANCELADA:
            color = "red"
        else:
            color = "grey"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, obj.get_estado_display())
    estado_formateado.short_description = _('Estado')
    estado_formateado.admin_order_field = 'estado'

    def costo_total_calculado(self, obj):
        # Vuelve a calcular por si acaso, o simplemente muestra el valor almacenado
        if obj.fecha_entrada and obj.fecha_salida and obj.habitacion:
            noches = (obj.fecha_salida - obj.fecha_entrada).days
            if noches > 0:
                return noches * obj.habitacion.precio_por_noche
        return "N/A" # O 0.00
    costo_total_calculado.short_description = _('Costo Calculado (referencia)')

    actions = ['marcar_como_confirmada', 'marcar_como_pendiente', 'marcar_como_cancelada']

    def marcar_como_confirmada(self, request, queryset):
        queryset.update(estado=Reserva.ESTADO_CONFIRMADA)
        self.message_user(request, _("Las reservas seleccionadas han sido marcadas como Confirmadas."))
    marcar_como_confirmada.short_description = _("Marcar seleccionadas como Confirmadas")

    def marcar_como_pendiente(self, request, queryset):
        queryset.update(estado=Reserva.ESTADO_PENDIENTE)
        self.message_user(request, _("Las reservas seleccionadas han sido marcadas como Pendientes."))
    marcar_como_pendiente.short_description = _("Marcar seleccionadas como Pendientes")

    def marcar_como_cancelada(self, request, queryset):
        queryset.update(estado=Reserva.ESTADO_CANCELADA)
        # Aquí podrías añadir lógica adicional, como liberar la habitación si fuera necesario.
        self.message_user(request, _("Las reservas seleccionadas han sido marcadas como Canceladas."))
    marcar_como_cancelada.short_description = _("Marcar seleccionadas como Canceladas")
