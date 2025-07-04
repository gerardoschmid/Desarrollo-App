# Contenido de servicios/admin.py
from django.contrib import admin
from .models import Servicio, CategoriaServicio
from django.utils.html import format_html

@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'orden', 'icono_fa_html_cat')
    search_fields = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('orden',)

    def icono_fa_html_cat(self, obj):
        if obj.icono_fa:
            return format_html('<i class="{}"></i> ({})', obj.icono_fa, obj.icono_fa)
        return "N/A"
    icono_fa_html_cat.short_description = 'Icono'


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_formateado', 'disponible', 'destacado', 'fecha_actualizacion', 'icono_fa_html_serv')
    list_filter = ('disponible', 'destacado', 'categoria', 'requiere_reserva_previa')
    search_fields = ('nombre', 'descripcion_corta', 'descripcion_larga', 'categoria__nombre')
    prepopulated_fields = {'slug': ('nombre',)}
    list_editable = ('disponible', 'destacado')
    autocomplete_fields = ['categoria'] # Si tienes muchas categorías
    list_select_related = ['categoria'] # Optimiza la consulta para categoría
    list_per_page = 25

    fieldsets = (
        (None, {
            'fields': ('nombre', 'slug', 'categoria', 'descripcion_corta', 'descripcion_larga')
        }),
        ('Visualización y Detalles Operativos', {
            'fields': ('icono_fa', 'imagen', 'horario_disponibilidad', 'ubicacion_especifica')
        }),
        ('Precio, Reserva y Estado', {
            'fields': ('precio', 'unidad_precio', 'requiere_reserva_previa', 'disponible', 'destacado')
        }),
        ("Fechas (Auditoría)", {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')

    def precio_formateado(self, obj):
        if obj.precio is not None:
            unidad = f" / {obj.get_unidad_precio_display()}" if obj.unidad_precio else ""
            return f"${obj.precio:,.2f}{unidad}"
        return "Consultar / Incluido"
    precio_formateado.short_description = "Precio"
    precio_formateado.admin_order_field = 'precio' # Permite ordenar por precio

    def icono_fa_html_serv(self, obj):
        if obj.icono_fa:
            return format_html('<i class="{}"></i> ({})', obj.icono_fa, obj.icono_fa)
        return "N/A"
    icono_fa_html_serv.short_description = 'Icono'

    # Añadir FontAwesome al admin para los iconos
    class Media:
        css = {
            'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',)
        }
```
