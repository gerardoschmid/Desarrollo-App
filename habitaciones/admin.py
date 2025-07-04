# Contenido de habitaciones/admin.py
from django.contrib import admin
from .models import TipoHabitacion, ImagenHabitacion, Habitacion, Amenidad

class ImagenHabitacionInline(admin.TabularInline): # o admin.StackedInline
    model = ImagenHabitacion
    extra = 1 # Número de formularios vacíos para imágenes adicionales
    fields = ('imagen', 'alt_text', 'orden')
    ordering = ['orden']
    verbose_name_plural = "Galería de Imágenes Adicionales"

class AmenidadesTipoHabitacionInline(admin.TabularInline):
    model = TipoHabitacion.amenidades.through # Acceder al modelo intermedio
    extra = 1
    verbose_name = "Amenidad Incluida"
    verbose_name_plural = "Amenidades Incluidas en este Tipo de Habitación"
    # Puedes usar autocomplete_fields si tienes muchas amenidades
    # autocomplete_fields = ['amenidad']


@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad_maxima', 'precio_base_noche_display', 'activo', 'destacado', 'fecha_actualizacion')
    list_filter = ('activo', 'destacado', 'capacidad_maxima')
    search_fields = ('nombre', 'descripcion')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('activo', 'destacado') # 'precio_base_noche' puede ser riesgoso editarlo en lista
    inlines = [ImagenHabitacionInline, AmenidadesTipoHabitacionInline]

    fieldsets = (
        (None, {
            'fields': ('nombre', 'slug', 'descripcion_corta', 'descripcion_larga', 'imagen_principal')
        }),
        ('Detalles y Precios', {
            'fields': ('capacidad_maxima', 'precio_base_noche', 'tipo_cama', 'tamano_habitacion_m2')
        }),
        ('Estado y Visibilidad', {
            'fields': ('activo', 'destacado')
        }),
        ("Fechas (Auditoría)", {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',), # Ocultar por defecto
        }),
    )
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    def precio_base_noche_display(self, obj):
        return f"${obj.precio_base_noche:,.2f}"
    precio_base_noche_display.short_description = "Precio Base"
    precio_base_noche_display.admin_order_field = 'precio_base_noche'

    def get_queryset(self, request):
        # Optimizar consulta si es necesario (ej. prefetch_related para amenidades o imágenes)
        return super().get_queryset(request).prefetch_related('amenidades', 'imagenes_adicionales')


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'tipo_habitacion', 'estado', 'piso', 'disponible_para_reserva')
    list_filter = ('estado', 'tipo_habitacion__nombre', 'piso', 'disponible_para_reserva')
    search_fields = ('numero', 'tipo_habitacion__nombre', 'caracteristicas_especiales')
    list_editable = ('estado', 'disponible_para_reserva')
    autocomplete_fields = ['tipo_habitacion'] # Mejora la selección si hay muchos tipos
    list_select_related = ['tipo_habitacion'] # Optimiza la consulta para el tipo de habitación
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('numero', 'tipo_habitacion', 'piso')
        }),
        ('Estado y Disponibilidad', {
            'fields': ('estado', 'disponible_para_reserva', 'caracteristicas_especiales')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('tipo_habitacion')

@admin.register(Amenidad)
class AmenidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'icono_fa_html', 'descripcion_corta')
    search_fields = ('nombre', 'descripcion')

    def descripcion_corta(self, obj):
        return (obj.descripcion[:50] + '...') if obj.descripcion and len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

    def icono_fa_html(self, obj):
        from django.utils.html import format_html
        if obj.icono_fa:
            return format_html('<i class="{}"></i> ({})', obj.icono_fa, obj.icono_fa)
        return "N/A"
    icono_fa_html.short_description = 'Icono'
    icono_fa_html.allow_tags = True # Necesario en versiones antiguas de Django, ahora format_html lo maneja


# No es necesario registrar ImagenHabitacion aquí si solo se usa como inline.
# Si quieres gestionarlas independientemente:
# @admin.register(ImagenHabitacion)
# class ImagenHabitacionAdmin(admin.ModelAdmin):
#     list_display = ('tipo_habitacion', 'alt_text', 'orden')
#     list_filter = ('tipo_habitacion',)
#     search_fields = ('alt_text', 'tipo_habitacion__nombre')
#     autocomplete_fields = ['tipo_habitacion']
```
