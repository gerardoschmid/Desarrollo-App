# Contenido de clientes/models.py
from django.db import models
from django.conf import settings # Para una posible relación futura con User
from django.core.exceptions import ValidationError
# from django_countries.fields import CountryField # Si decides usar django-countries

class Cliente(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('DNI', 'DNI (Documento Nacional de Identidad)'),
        ('PAS', 'Pasaporte'),
        ('CE', 'Cédula de Extranjería'),
        ('RIF', 'RIF (Registro de Información Fiscal - Venezuela)'),
        ('NIT', 'NIT (Número de Identificación Tributaria)'),
        ('OTR', 'Otro'),
    ]

    # Relación opcional con el modelo User de Django
    # user = models.OneToOneField(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True, blank=True,
    #     verbose_name="Usuario Asociado (Login)",
    #     help_text="Si el cliente tiene una cuenta de usuario en el sistema."
    # )

    nombre_completo = models.CharField(max_length=150, verbose_name="Nombre Completo")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico", help_text="Debe ser único para cada cliente.")
    telefono = models.CharField(max_length=25, blank=True, verbose_name="Número de Teléfono Principal")
    telefono_alternativo = models.CharField(max_length=25, blank=True, verbose_name="Teléfono Alternativo")

    tipo_documento = models.CharField(
        max_length=5,
        choices=TIPO_DOCUMENTO_CHOICES,
        blank=True, null=True,
        verbose_name="Tipo de Documento"
    )
    numero_documento = models.CharField(max_length=30, blank=True, verbose_name="Número de Documento")

    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")

    # Podrías usar django-countries para un campo de país más robusto:
    # pais_residencia = CountryField(blank=True, null=True, verbose_name="País de Residencia")
    pais_residencia = models.CharField(max_length=100, blank=True, verbose_name="País de Residencia")
    ciudad_residencia = models.CharField(max_length=100, blank=True, verbose_name="Ciudad de Residencia")
    direccion_completa = models.TextField(blank=True, verbose_name="Dirección Completa")

    notas_internas = models.TextField(blank=True, verbose_name="Notas Internas (Solo Admin)", help_text="Información relevante para el personal del hotel sobre este cliente.")

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    ultima_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    # historial_reservas se obtiene a través de la relación inversa desde el modelo Reserva.
    # el related_name en el modelo Reserva para el ForeignKey a Cliente debe ser 'reservas_cliente' o similar.

    def __str__(self):
        return f"{self.nombre_completo} ({self.email})"

    def clean(self):
        super().clean()
        # Validar que el número de documento sea único para el tipo de documento (si ambos están presentes)
        if self.tipo_documento and self.numero_documento:
            queryset = Cliente.objects.filter(
                tipo_documento=self.tipo_documento,
                numero_documento=self.numero_documento
            ).exclude(pk=self.pk) # Excluir el propio objeto si se está editando
            if queryset.exists():
                raise ValidationError({
                    'numero_documento': f"Ya existe un cliente con este tipo y número de documento ({self.get_tipo_documento_display()}: {self.numero_documento})."
                })

        # Validar edad (opcional, ejemplo)
        # if self.fecha_nacimiento:
        #     from datetime import date
        #     today = date.today()
        #     age = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        #     if age < 18:
        #         raise ValidationError({'fecha_nacimiento': "El cliente debe ser mayor de edad."})


    @property
    def cantidad_reservas_realizadas(self):
        # Asegúrate que el related_name en la ForeignKey de Reserva a Cliente sea 'reservas_cliente'
        return self.reservas_cliente.count()

    @property
    def ultima_reserva_fecha(self):
        ultima = self.reservas_cliente.order_by('-fecha_creacion').first()
        return ultima.fecha_creacion if ultima else None

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nombre_completo']
        # Restricción a nivel de base de datos para combinación de tipo y número de documento
        # unique_together = [['tipo_documento', 'numero_documento']] # Cuidado con valores NULL si son permitidos
        constraints = [
            models.UniqueConstraint(fields=['tipo_documento', 'numero_documento'], name='unique_tipo_numero_documento', condition=models.Q(tipo_documento__isnull=False) & models.Q(numero_documento__isnull=False) & ~models.Q(numero_documento=''))
        ]
```
