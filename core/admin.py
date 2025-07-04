# Contenido de core/admin.py
from django.contrib import admin
from .models import ConfiguracionSitio, ImagenGaleria, MensajeContacto

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ('nombre_hotel', 'telefono_contacto', 'email_contacto')
    # Solo permitir una instancia de configuración
    def has_add_permission(self, request):
        # Permite añadir si no existe ninguna configuración.
        # Si ya existe una, no permite añadir más.
        return not ConfiguracionSitio.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # No permitir borrar la configuración desde el admin.
        return False

@admin.register(ImagenGaleria)
class ImagenGaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo_display', 'orden', 'descripcion_corta_display')
    list_editable = ('orden',)
    search_fields = ('titulo', 'descripcion')
    list_per_page = 20

    def titulo_display(self, obj):
        return obj.titulo or f"Imagen ID: {obj.id}"
    titulo_display.short_description = 'Título / ID'

    def descripcion_corta_display(self, obj):
        return (obj.descripcion[:75] + '...') if obj.descripcion and len(obj.descripcion) > 75 else obj.descripcion
    descripcion_corta_display.short_description = 'Descripción'


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'asunto', 'fecha_creacion', 'leido')
    list_filter = ('leido', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'fecha_creacion')
    list_per_page = 20
    date_hierarchy = 'fecha_creacion'

    fieldsets = (
        (None, {
            'fields': ('nombre', 'email', 'asunto', 'mensaje')
        }),
        ('Estado y Auditoría', {
            'fields': ('leido', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        # No permitir añadir mensajes desde el admin, deben venir del formulario público
        return False

    def has_change_permission(self, request, obj=None):
        # Permitir cambiar el estado 'leido', pero no el contenido del mensaje
        if obj is not None: # Si es una vista de cambio de un objeto existente
             return True # Permite cambiar 'leido'
        return super().has_change_permission(request, obj) # Comportamiento por defecto para la vista de lista
