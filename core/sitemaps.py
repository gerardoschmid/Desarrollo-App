# Contenido de core/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from habitaciones.models import TipoHabitacion # Asumiendo que este es el modelo a mostrar
from servicios.models import Servicio # Asumiendo que este es el modelo a mostrar

class StaticViewSitemap(Sitemap):
    priority = 0.9 # Prioridad más alta para páginas estáticas principales
    changefreq = 'weekly' # Con qué frecuencia es probable que cambie el contenido

    def items(self):
        # Lista de nombres de URL para las vistas estáticas que quieres en el sitemap
        return [
            'core:index',
            'core:about',
            'core:contact',
            'core:gallery',
            'habitaciones:lista_tipos_habitacion', # Página principal de listado de habitaciones
            'servicios:lista_servicios',       # Página principal de listado de servicios
            'reservas:crear_reserva'           # Página del formulario de reserva
        ]

    def location(self, item):
        # Devuelve la URL para cada 'item'
        return reverse(item)

class HabitacionSitemap(Sitemap):
    changefreq = "daily" # Si las habitaciones cambian de estado o precio con frecuencia
    priority = 0.7

    def items(self):
        # Devuelve todos los objetos TipoHabitacion que estén activos
        return TipoHabitacion.objects.filter(activo=True)

    def lastmod(self, obj):
        # Devuelve la fecha de última modificación del objeto
        # Asegúrate de que tu modelo TipoHabitacion tenga un campo como 'fecha_actualizacion'
        return obj.fecha_actualizacion # Si no tienes, puedes omitir este método o usar fecha_creacion

    # Django usará el método get_absolute_url() de tu modelo TipoHabitacion por defecto
    # para la etiqueta <loc>. Si no lo tienes, debes implementar location(self, obj).
    # def location(self, obj):
    #     return obj.get_absolute_url()


class ServicioSitemap(Sitemap):
    changefreq = "monthly" # Si los servicios no cambian tan a menudo
    priority = 0.6

    def items(self):
        return Servicio.objects.filter(disponible=True)

    def lastmod(self, obj):
        return obj.fecha_actualizacion # Asume campo 'fecha_actualizacion'

    # Django usará el método get_absolute_url() de tu modelo Servicio por defecto.
    # def location(self, obj):
    #     return obj.get_absolute_url()

# Nota: Si tienes más modelos que quieres incluir en el sitemap (ej. posts de un blog),
# crea una clase Sitemap similar para cada uno y añádela al diccionario 'sitemaps'
# en tu archivo urls.py principal (hotel_project/urls.py).
