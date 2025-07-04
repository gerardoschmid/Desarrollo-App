from django.db import models
from django.utils.translation import gettext_lazy as _

# Ejemplo: Modelo para un banner o promoción en la página de inicio
# class Promocion(models.Model):
#     titulo = models.CharField(_("Título"), max_length=200)
#     descripcion = models.TextField(_("Descripción"))
#     imagen = models.ImageField(_("Imagen de Fondo"), upload_to='promociones/', null=True, blank=True)
#     enlace_destino = models.URLField(_("Enlace de Destino"), blank=True, null=True)
#     activa = models.BooleanField(_("Activa"), default=True)
#     orden = models.PositiveIntegerField(_("Orden de Visualización"), default=0)

#     class Meta:
#         verbose_name = _("Promoción")
#         verbose_name_plural = _("Promociones")
#         ordering = ['orden', 'titulo']

#     def __str__(self):
#         return self.titulo

# Por ahora, la app core no tendrá modelos propios específicos,
# ya que su función principal será la presentación y páginas estáticas.
# Si se necesita contenido dinámico gestionable para estas páginas (ej. testimonios, FAQs),
# se podrían añadir modelos aquí.
