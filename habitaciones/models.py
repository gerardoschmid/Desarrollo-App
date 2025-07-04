# Contenido de habitaciones/models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import format_html # Para mostrar iconos en el admin, por ejemplo

class Amenidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Amenidad")
    descripcion = models.TextField(blank=True, verbose_name="Descripción (Opcional)")
    icono_fa = models.CharField(max_length=50, blank=True, help_text="Clase de FontAwesome (ej: 'fas fa-wifi', 'fas fa-tv'). Visita fontawesome.com/icons", verbose_name="Icono FontAwesome")

    def __str__(self):
        return self.nombre

    def display_icon(self):
        if self.icono_fa:
            return format_html('<i class="{}"></i>', self.icono_fa)
        return ""
    display_icon.short_description = "Icono"

    class Meta:
        verbose_name = "Amenidad de Habitación"
        verbose_name_plural = "Amenidades de Habitación"
        ordering = ['nombre']


class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Tipo")
    slug = models.SlugField(max_length=120, unique=True, blank=True, help_text="Generado automáticamente si se deja en blanco. Usado en la URL.")
    descripcion_corta = models.CharField(max_length=255, blank=True, help_text="Un resumen breve para listados y tarjetas.", verbose_name="Descripción Corta")
    descripcion_larga = models.TextField(verbose_name="Descripción Detallada")

    imagen_principal = models.ImageField(
        upload_to='tipos_habitacion/principales/',
        blank=True, null=True,
        verbose_name="Imagen Principal",
        help_text="La imagen más representativa de este tipo de habitación."
    )

    capacidad_maxima = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Capacidad Máxima",
        help_text="Número máximo de huéspedes permitidos."
    )
    precio_base_noche = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Precio Base por Noche (USD)", # Asumiendo USD, ajustar si es otra moneda
        help_text="Precio estándar antes de impuestos o cargos adicionales."
    )

    tipo_cama = models.CharField(max_length=100, blank=True, verbose_name="Tipo de Cama(s)", help_text="Ej: '1 King Size', '2 Dobles', '1 Queen + 1 Sofá Cama'")
    tamano_habitacion_m2 = models.DecimalField(
        max_digits=5, decimal_places=1,
        blank=True, null=True,
        verbose_name="Tamaño de Habitación (m²)",
        help_text="Tamaño aproximado en metros cuadrados."
    )

    amenidades = models.ManyToManyField(
        Amenidad,
        blank=True,
        related_name="tipos_habitacion",
        verbose_name="Amenidades Incluidas"
    )

    activo = models.BooleanField(default=True, verbose_name="¿Está activo y visible para reservas?")
    destacado = models.BooleanField(default=False, verbose_name="¿Destacar en la página principal o listados especiales?")

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        # Asegurar que el slug sea único incluso si se edita el nombre
        original_slug = self.slug
        queryset = TipoHabitacion.objects.filter(slug=self.slug).exclude(pk=self.pk)
        counter = 1
        while queryset.exists():
            self.slug = f"{original_slug}-{counter}"
            queryset = TipoHabitacion.objects.filter(slug=self.slug).exclude(pk=self.pk)
            counter += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('habitaciones:detalle_tipo_habitacion', kwargs={'slug': self.slug})

    def get_precio_formateado(self):
        # return f"${self.precio_base_noche:,.2f}" # Formato con comas para miles
        return f"{self.precio_base_noche:.2f}" # Formato simple con dos decimales

    class Meta:
        verbose_name = "Tipo de Habitación"
        verbose_name_plural = "Tipos de Habitación"
        ordering = ['nombre']


class ImagenHabitacion(models.Model):
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        related_name='imagenes_adicionales',
        on_delete=models.CASCADE,
        verbose_name="Tipo de Habitación Asociado"
    )
    imagen = models.ImageField(upload_to='tipos_habitacion/galeria/', verbose_name="Imagen Adicional")
    alt_text = models.CharField(max_length=150, blank=True, verbose_name="Texto Alternativo (SEO)", help_text="Descripción breve de la imagen para accesibilidad y SEO.")
    orden = models.PositiveIntegerField(default=0, help_text="Para ordenar las imágenes en la galería del tipo de habitación (menor a mayor).", verbose_name="Orden de Visualización")

    def __str__(self):
        return f"Imagen para {self.tipo_habitacion.nombre} (ID: {self.id})"

    class Meta:
        verbose_name = "Imagen Adicional de Tipo de Habitación"
        verbose_name_plural = "Galería de Imágenes de Tipos de Habitación"
        ordering = ['tipo_habitacion', 'orden']


class Habitacion(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupada', 'Ocupada'),
        ('mantenimiento', 'En Mantenimiento'),
        ('limpieza', 'En Limpieza'),
        ('bloqueada', 'Bloqueada (No Usar)'),
    ]
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Habitación", help_text="Identificador único de la habitación física (ej: 101, 20A).")
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.PROTECT, # Evitar borrar Tipo si hay Habitaciones asignadas
        related_name='habitaciones_fisicas',
        verbose_name="Tipo de Habitación"
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible', verbose_name="Estado Actual")
    piso = models.CharField(max_length=10, blank=True, verbose_name="Piso/Ubicación", help_text="Ej: 'Planta Baja', 'Piso 3', 'Ala Norte'.")
    caracteristicas_especiales = models.TextField(blank=True, help_text="Características únicas de esta habitación física específica (ej. 'Con balcón y vistas al jardín', 'Adaptada para movilidad reducida').", verbose_name="Notas / Características Especiales")
    disponible_para_reserva = models.BooleanField(default=True, verbose_name="¿Disponible para nuevas reservas?", help_text="Desmarcar si la habitación no debe ser considerada para el sistema de reservas temporalmente (ej. reparaciones menores no clasificadas como 'mantenimiento' total).")

    def __str__(self):
        return f"Habitación N° {self.numero} ({self.tipo_habitacion.nombre})"

    @property
    def esta_realmente_disponible(self):
        """Considera tanto el estado como la bandera 'disponible_para_reserva'."""
        return self.estado == 'disponible' and self.disponible_para_reserva

    class Meta:
        verbose_name = "Habitación Física"
        verbose_name_plural = "Habitaciones Físicas (Inventario)"
        ordering = ['numero']
```
