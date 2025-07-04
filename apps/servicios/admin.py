from django.contrib import admin
from .models import Servicio
from django.utils.translation import gettext_lazy as _

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'disponible', 'created_at', 'updated_at')
    list_filter = ('disponible', 'created_at')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'disponible')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'precio')
        }),
        (_('Disponibilidad e Imagen'), {
            'fields': ('disponible', 'imagen')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',), # Opcional: colapsar esta sección
        }),
    )
