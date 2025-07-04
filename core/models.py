# Contenido de core/models.py
from django.db import models
from django.urls import reverse

class ConfiguracionSitio(models.Model):
    nombre_hotel = models.CharField(max_length=100, default="Hotel Premium MVP", verbose_name="Nombre del Hotel")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True, help_text="Logo principal del hotel (idealmente formato PNG transparente o SVG). Se mostrará en el navbar.", verbose_name="Logo del Hotel")
    favicon = models.ImageField(upload_to='logos/favicons/', blank=True, null=True, help_text="Icono para la pestaña del navegador (formato .ico, .png, .svg).", verbose_name="Favicon")
    telefono_contacto = models.CharField(max_length=25, blank=True, help_text="Teléfono principal de contacto del hotel.", verbose_name="Teléfono de Contacto")
    email_contacto = models.EmailField(blank=True, help_text="Email principal de contacto del hotel.", verbose_name="Email de Contacto")
    direccion = models.TextField(blank=True, help_text="Dirección física completa del hotel.", verbose_name="Dirección del Hotel")
    descripcion_corta_meta = models.TextField(blank=True, help_text="Descripción corta para SEO (meta description, idealmente ~155 caracteres). Aparecerá en resultados de búsqueda.", verbose_name="Meta Descripción (SEO)")
    palabras_clave_meta = models.CharField(max_length=255, blank=True, help_text="Palabras clave para SEO (separadas por comas).", verbose_name="Meta Palabras Clave (SEO)")

    texto_hero_principal = models.CharField(max_length=150, blank=True, default="Bienvenido a Tu Hogar Lejos de Casa", verbose_name="Título Principal (Hero Section)")
    texto_hero_secundario = models.TextField(blank=True, default="Descubre el confort y la hospitalidad que nos caracteriza. Reserva tu estancia hoy mismo.", verbose_name="Subtítulo (Hero Section)")
    imagen_hero_background = models.ImageField(upload_to='hero_images/', blank=True, null=True, help_text="Imagen de fondo para la sección principal de la página de inicio.", verbose_name="Imagen de Fondo (Hero)")

    facebook_url = models.URLField(blank=True, null=True, verbose_name="Enlace a Facebook")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Enlace a Instagram")
    twitter_url = models.URLField(blank=True, null=True, verbose_name="Enlace a Twitter (X)")
    # Otros campos como YouTube, LinkedIn, etc.

    def __str__(self):
        return f"Configuración de {self.nombre_hotel}"

    class Meta:
        verbose_name = "1. Configuración del Sitio" # El número ayuda a ordenar en el admin
        verbose_name_plural = "1. Configuraciones del Sitio"

    # Solo debe existir una instancia de este modelo.
    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionSitio.objects.exists():
            # Si se está creando una nueva instancia y ya existe una, no permitir.
            # Esto es una salvaguarda, el admin ya lo previene.
            raise ValidationError('Solo puede existir una instancia de Configuración del Sitio.')
        return super(ConfiguracionSitio, self).save(*args, **kwargs)


class ImagenGaleria(models.Model):
    titulo = models.CharField(max_length=100, blank=True, verbose_name="Título de la Imagen")
    imagen = models.ImageField(upload_to='galeria_hotel/', verbose_name="Archivo de Imagen")
    descripcion = models.TextField(blank=True, verbose_name="Descripción (Opcional)")
    orden = models.PositiveIntegerField(default=0, help_text="Determina el orden de aparición en la galería (menor a mayor).", verbose_name="Orden de Visualización")
    alt_text = models.CharField(max_length=150, blank=True, help_text="Texto alternativo para accesibilidad y SEO.", verbose_name="Texto Alternativo (alt)")

    def __str__(self):
        return self.titulo or f"Imagen ID: {self.id}"

    class Meta:
        verbose_name = "Imagen de Galería del Hotel"
        verbose_name_plural = "Imágenes de Galería del Hotel"
        ordering = ['orden', 'titulo']


class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Remitente")
    email = models.EmailField(verbose_name="Email del Remitente")
    asunto = models.CharField(max_length=200, verbose_name="Asunto del Mensaje")
    mensaje = models.TextField(verbose_name="Contenido del Mensaje")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Recepción")
    leido = models.BooleanField(default=False, verbose_name="¿Mensaje Leído?")

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.email}) sobre '{self.asunto}' - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Mensaje de Contacto Recibido"
        verbose_name_plural = "Mensajes de Contacto Recibidos"
        ordering = ['-fecha_creacion'] # Los más recientes primero
        permissions = [
            ("can_mark_as_read", "Puede marcar mensajes como leídos"),
        ]
