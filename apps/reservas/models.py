from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.habitaciones.models import Habitacion
from apps.clientes.models import Cliente
from django.core.exceptions import ValidationError
from django.utils import timezone

class Reserva(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_COMPLETADA = 'completada' # Huésped hizo check-out

    ESTADOS_RESERVA = [
        (ESTADO_PENDIENTE, _('Pendiente')),
        (ESTADO_CONFIRMADA, _('Confirmada')),
        (ESTADO_CANCELADA, _('Cancelada')),
        (ESTADO_COMPLETADA, _('Completada')),
    ]

    habitacion = models.ForeignKey(Habitacion, on_delete=models.PROTECT, verbose_name=_("Habitación")) # PROTECT para no borrar habitación si tiene reservas
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name=_("Cliente"))

    fecha_entrada = models.DateField(_("Fecha de Entrada"))
    fecha_salida = models.DateField(_("Fecha de Salida"))

    numero_huespedes = models.PositiveIntegerField(_("Número de Huéspedes"), default=1)

    estado = models.CharField(
        _("Estado de la Reserva"),
        max_length=20,
        choices=ESTADOS_RESERVA,
        default=ESTADO_PENDIENTE
    )

    costo_total = models.DecimalField(_("Costo Total"), max_digits=10, decimal_places=2, null=True, blank=True, help_text=_("Calculado automáticamente si no se provee."))
    notas_adicionales = models.TextField(_("Notas Adicionales"), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Reserva")
        verbose_name_plural = _("Reservas")
        ordering = ['-fecha_entrada', '-created_at']

    def __str__(self):
        return f"Reserva de {self.cliente} para {self.habitacion} ({self.fecha_entrada} a {self.fecha_salida})"

    def clean(self):
        # Validación de fechas
        if self.fecha_entrada and self.fecha_salida:
            if self.fecha_salida <= self.fecha_entrada:
                raise ValidationError(_("La fecha de salida debe ser posterior a la fecha de entrada."))
            if self.fecha_entrada < timezone.now().date():
                # Permitir si es una reserva histórica o si se está editando una reserva pasada
                # Para nuevas reservas, usualmente no se permite fecha de entrada en el pasado
                # raise ValidationError(_("La fecha de entrada no puede ser en el pasado."))
                pass # Se puede ajustar esta lógica según sea necesario

        # Validación de capacidad
        if self.numero_huespedes and self.habitacion:
            if self.numero_huespedes > self.habitacion.capacidad:
                raise ValidationError(
                    _("El número de huéspedes (%(num_huespedes)s) excede la capacidad de la habitación (%(capacidad)s).") %
                    {'num_huespedes': self.numero_huespedes, 'capacidad': self.habitacion.capacidad}
                )

        # Validación de disponibilidad (más compleja, usualmente se maneja en el form o view)
        # Aquí se podría añadir una validación básica si no hay otras reservas que se solapen.
        # Sin embargo, una validación completa de solapamiento es mejor en la lógica de negocio de la vista/formulario.
        # Ejemplo básico (no exhaustivo y puede necesitar optimización para muchas reservas):
        # reservas_solapadas = Reserva.objects.filter(
        #     habitacion=self.habitacion,
        #     estado__in=[self.ESTADO_CONFIRMADA, self.ESTADO_PENDIENTE] # Considerar solo reservas activas
        # ).exclude(pk=self.pk).filter(
        #     fecha_entrada__lt=self.fecha_salida,
        #     fecha_salida__gt=self.fecha_entrada
        # )
        # if reservas_solapadas.exists():
        #     raise ValidationError(_("La habitación no está disponible para las fechas seleccionadas."))


    def save(self, *args, **kwargs):
        if not self.costo_total:
            # Calcular costo total si no se proporciona
            if self.fecha_entrada and self.fecha_salida and self.habitacion:
                noches = (self.fecha_salida - self.fecha_entrada).days
                if noches > 0:
                    self.costo_total = noches * self.habitacion.precio_por_noche
                else:
                    self.costo_total = self.habitacion.precio_por_noche # Mínimo una noche
        super().save(*args, **kwargs)

    @property
    def duracion_estancia(self):
        if self.fecha_entrada and self.fecha_salida:
            return (self.fecha_salida - self.fecha_entrada).days
        return 0
