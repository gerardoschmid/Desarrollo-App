# Contenido de servicios/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator

class CategoriaServicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="Generado automáticamente. Usado en URL.")
    descripcion = models.TextField(blank=True, verbose_name="Descripción (Opcional)")
    icono_fa = models.CharField(max_length=50, blank=True, help_text="Clase de FontAwesome (ej: 'fas fa-utensils').", verbose_name="Icono FontAwesome")
    orden = models.PositiveIntegerField(default=0, help_text="Orden de aparición (menor a mayor).", verbose_name="Orden")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Categoría de Servicio"
        verbose_name_plural = "Categorías de Servicios"
        ordering = ['orden', 'nombre']


class Servicio(models.Model):
    UNIDAD_PRECIO_CHOICES = [
        ('unico', 'Pago Único'),
        ('persona', 'Por Persona'),
        ('hora', 'Por Hora'),
        ('dia', 'Por Día'),
        ('noche', 'Por Noche'),
        ('evento', 'Por Evento/Servicio Completo'),
    ]

    categoria = models.ForeignKey(
        CategoriaServicio,
        on_delete=models.SET_NULL, # Si se borra categoría, el servicio queda sin categoría pero no se borra
        null=True, blank=True,
        related_name='servicios',
        verbose_name="Categoría del Servicio"
    )
    nombre = models.CharField(max_length=150, unique=True, verbose_name="Nombre del Servicio")
    slug = models.SlugField(max_length=170, unique=True, blank=True, help_text="Generado automáticamente. Usado en URL.")
    descripcion_corta = models.CharField(max_length=255, blank=True, verbose_name="Descripción Corta (para listados)")
    descripcion_larga = models.TextField(verbose_name="Descripción Detallada")

    icono_fa = models.CharField(max_length=50, blank=True, help_text="Clase de FontAwesome (ej: 'fas fa-spa', 'fas fa-concierge-bell').", verbose_name="Icono FontAwesome")
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True, verbose_name="Imagen Representativa del Servicio")

    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0.00)],
        verbose_name="Precio (si aplica)",
        help_text="Dejar en blanco si el servicio está incluido o el precio es variable (consultar)."
    )
    unidad_precio = models.CharField(
        max_length=10,
        choices=UNIDAD_PRECIO_CHOICES,
        default='unico',
        verbose_name="Unidad del Precio",
        help_text="Cómo se cobra el precio (si aplica)."
    )

    disponible = models.BooleanField(default=True, verbose_name="¿Está disponible actualmente?")
    destacado = models.BooleanField(default=False, verbose_name="¿Destacar en la página principal o listados?")
    requiere_reserva_previa = models.BooleanField(default=False, verbose_name="¿Requiere reserva previa?", help_text="Marcar si el cliente necesita reservar este servicio con antelación.")

    horario_disponibilidad = models.CharField(max_length=150, blank=True, verbose_name="Horario de Disponibilidad", help_text="Ej: 'Lunes a Viernes de 9am a 5pm', '24/7'.")
    ubicacion_especifica = models.CharField(max_length=150, blank=True, verbose_name="Ubicación Específica", help_text="Ej: 'Piscina Principal', 'Restaurante El Mirador', 'Recepción'.")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        # Asegurar slug único
        original_slug = self.slug
        queryset = Servicio.objects.filter(slug=self.slug).exclude(pk=self.pk)
        counter = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = Servicio.objects.filter(slug=self.slug).exclude(pk=self.pk)
            counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Asume que tienes una vista de detalle para servicios
        return reverse('servicios:detalle_servicio', kwargs={'slug': self.slug})

    def get_precio_display_completo(self):
        if self.precio is not None:
            return f"${self.precio:,.2f} ({self.get_unidad_precio_display()})"
        return "Consultar"

    class Meta:
        verbose_name = "Servicio del Hotel"
        verbose_name_plural = "Servicios del Hotel"
        ordering = ['categoria__orden', 'nombre'] # Ordenar por categoría y luego por nombre
```
