from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.servicios.models import Servicio # Asumiendo que algunos servicios pueden ser específicos de habitaciones

class TipoHabitacion(models.Model):
    nombre = models.CharField(_("Nombre del Tipo"), max_length=100, unique=True)
    descripcion = models.TextField(_("Descripción"), blank=True, null=True)

    class Meta:
        verbose_name = _("Tipo de Habitación")
        verbose_name_plural = _("Tipos de Habitación")
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Habitacion(models.Model):
    numero_habitacion = models.CharField(_("Número de Habitación"), max_length=10, unique=True)
    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT, verbose_name=_("Tipo de Habitación"))
    capacidad = models.PositiveIntegerField(_("Capacidad"))
    precio_por_noche = models.DecimalField(_("Precio por Noche"), max_digits=10, decimal_places=2)
    disponible = models.BooleanField(_("Disponible"), default=True, help_text=_("Indica si la habitación está disponible para reservas en general."))
    descripcion_adicional = models.TextField(_("Descripción Adicional"), blank=True, null=True)
    # Podríamos tener un campo ManyToMany a Servicio si las habitaciones pueden tener características específicas como 'servicios incluidos'
    # caracteristicas_especiales = models.ManyToManyField(Servicio, blank=True, verbose_name=_("Características Especiales"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Habitación")
        verbose_name_plural = _("Habitaciones")
        ordering = ['numero_habitacion']

    def __str__(self):
        return f"{self.tipo_habitacion.nombre} - {self.numero_habitacion}"

class ImagenHabitacion(models.Model):
    habitacion = models.ForeignKey(Habitacion, related_name='imagenes', on_delete=models.CASCADE, verbose_name=_("Habitación"))
    imagen = models.ImageField(_("Imagen"), upload_to='habitaciones/')
    descripcion_imagen = models.CharField(_("Descripción de la Imagen"), max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Imagen de Habitación")
        verbose_name_plural = _("Imágenes de Habitación")
        ordering = ['created_at']

    def __str__(self):
        return f"Imagen para {self.habitacion.numero_habitacion}"
