# core/context_processors.py

from .models import ConfiguracionSitio

def site_config(request):
    """
    Añade la instancia de ConfiguracionSitio al contexto de todas las plantillas.
    """
    config = ConfiguracionSitio.objects.first()
    # Si no hay configuración, 'config' será None.
    # Las plantillas pueden manejar esto usando {{ config.nombre_hotel|default:"Valor por defecto" }}
    return {'config': config}
