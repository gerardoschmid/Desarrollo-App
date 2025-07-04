from django.contrib import admin
from .models import TipoHabitacion, Habitacion, ImagenHabitacion
from django.utils.translation import gettext_lazy as _

class ImagenHabitacionInline(admin.TabularInline): # O admin.StackedInline
    model = ImagenHabitacion
    extra = 1 # Número de formularios vacíos para añadir imágenes
    readonly_fields = ('created_at',)
    fields = ('imagen', 'descripcion_imagen', 'created_at')

@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_cantidad_habitaciones')
    search_fields = ('nombre', 'descripcion')

    def get_cantidad_habitaciones(self, obj):
        return obj.habitacion_set.count()
    get_cantidad_habitaciones.short_description = _('Cantidad de Habitaciones')

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero_habitacion', 'tipo_habitacion', 'capacidad', 'precio_por_noche', 'disponible', 'updated_at')
    list_filter = ('disponible', 'tipo_habitacion', 'capacidad')
    search_fields = ('numero_habitacion', 'tipo_habitacion__nombre', 'descripcion_adicional')
    list_editable = ('precio_por_noche', 'disponible')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ImagenHabitacionInline]

    fieldsets = (
        (None, {
            'fields': ('numero_habitacion', 'tipo_habitacion', 'capacidad', 'precio_por_noche')
        }),
        (_('Detalles y Disponibilidad'), {
            'fields': ('disponible', 'descripcion_adicional')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    # Si tienes muchos tipos de habitación, un raw_id_fields puede ser útil para el ForeignKey
    # raw_id_fields = ('tipo_habitacion',)

@admin.register(ImagenHabitacion)
class ImagenHabitacionAdmin(admin.ModelAdmin):
    list_display = ('habitacion', 'descripcion_imagen', 'get_thumbnail', 'created_at')
    list_filter = ('habitacion__tipo_habitacion',)
    search_fields = ('habitacion__numero_habitacion', 'descripcion_imagen')
    readonly_fields = ('created_at', 'get_thumbnail')

    fieldsets = (
        (None, {
            'fields': ('habitacion', 'imagen', 'get_thumbnail', 'descripcion_imagen')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    def get_thumbnail(self, obj):
        from django.utils.html import format_html
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.imagen.url)
        return "-"
    get_thumbnail.short_description = _('Miniatura')
