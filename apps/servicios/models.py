from django.db import models
from django.utils.translation import gettext_lazy as _

class Servicio(models.Model):
    nombre = models.CharField(_("Nombre del Servicio"), max_length=100, unique=True)
    descripcion = models.TextField(_("Descripción"))
    precio = models.DecimalField(_("Precio"), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_("Dejar en blanco si el servicio es gratuito."))
    imagen = models.ImageField(_("Imagen"), upload_to='servicios/', null=True, blank=True)
    disponible = models.BooleanField(_("Disponible"), default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Servicio")
        verbose_name_plural = _("Servicios")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('servicios:detalle_servicio', kwargs={'pk': self.pk})
