from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.habitaciones.models import TipoHabitacion
from apps.servicios.models import Servicio
# from apps.blog.models import Post # Si tuvieras un blog, por ejemplo

class StaticViewSitemap(Sitemap):
    """Sitemap para páginas estáticas principales."""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        # Lista de nombres de URL de tus vistas estáticas
        return [
            'core:inicio',
            'core:sobre_nosotros',
            'core:contacto',
            'core:galeria',
            'habitaciones:lista_tipos_habitacion', # Considerada una página principal de listado
            'servicios:lista_servicios', # Considerada una página principal de listado
            'reservas:crear_reserva', # Página principal para iniciar una reserva
        ]

    def location(self, item):
        return reverse(item)

class TipoHabitacionSitemap(Sitemap):
    """Sitemap para los detalles de los Tipos de Habitación."""
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return TipoHabitacion.objects.all()

    def lastmod(self, obj):
        # Asumimos que TipoHabitacion no tiene un campo 'updated_at'.
        # Si lo tuviera, se usaría obj.updated_at.
        # Podríamos buscar la última modificación de una habitación de ese tipo.
        # Por simplicidad, si no hay un campo de modificación en TipoHabitacion,
        # podríamos omitir lastmod o usar una fecha fija o la del sitio.
        # Para este ejemplo, lo omitiremos. Si se requiere, se puede añadir lógica.
        return None

    # def location(self, obj): # Django infiere esto de get_absolute_url si existe
    #     return reverse('habitaciones:detalle_tipo_habitacion', kwargs={'pk': obj.pk})
    # Es mejor definir get_absolute_url en el modelo TipoHabitacion.

class ServicioSitemap(Sitemap):
    """Sitemap para los detalles de los Servicios."""
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Servicio.objects.filter(disponible=True)

    def lastmod(self, obj):
        return obj.updated_at # Asumiendo que Servicio tiene updated_at

    # def location(self, obj):
    #     return reverse('servicios:detalle_servicio', kwargs={'pk': obj.pk})
    # Es mejor definir get_absolute_url en el modelo Servicio.


# Si tuvieras más modelos dinámicos que quieras incluir, como posts de un blog:
# class PostSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.9
#     def items(self):
#         return Post.objects.filter(status='published')
#     def lastmod(self, obj):
#         return obj.updated_at


# Diccionario de sitemaps para registrar en urls.py
sitemaps = {
    'static': StaticViewSitemap,
    'tipos_habitacion': TipoHabitacionSitemap,
    'servicios': ServicioSitemap,
    # 'blog': PostSitemap, # Si existiera
}
