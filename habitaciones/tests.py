# Contenido de habitaciones/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from .models import TipoHabitacion, Habitacion, Amenidad, ImagenHabitacion
from core.models import ConfiguracionSitio # Importar si las vistas lo usan para el contexto global

class AmenidadModelTestCase(TestCase):
    def test_amenidad_creacion(self):
        amenidad = Amenidad.objects.create(nombre="WiFi Gratuito", icono_fa="fas fa-wifi")
        self.assertEqual(str(amenidad), "WiFi Gratuito")
        self.assertTrue(amenidad.display_icon().startswith('<i class="fas fa-wifi"></i>'))

class TipoHabitacionModelTestCase(TestCase):
    def setUp(self):
        self.amenidad1 = Amenidad.objects.create(nombre="Aire Acondicionado")
        self.tipo_estandar = TipoHabitacion.objects.create(
            nombre="Estándar Deluxe",
            descripcion_larga="Habitación cómoda y funcional con vista.",
            capacidad_maxima=2,
            precio_base_noche=100.00
        )
        self.tipo_estandar.amenidades.add(self.amenidad1)

    def test_tipo_habitacion_creacion_y_slug(self):
        self.assertEqual(self.tipo_estandar.nombre, "Estándar Deluxe")
        self.assertEqual(self.tipo_estandar.slug, slugify("Estándar Deluxe"))
        self.assertEqual(str(self.tipo_estandar), "Estándar Deluxe")

    def test_tipo_habitacion_get_absolute_url(self):
        expected_url = reverse('habitaciones:detalle_tipo_habitacion', kwargs={'slug': self.tipo_estandar.slug})
        self.assertEqual(self.tipo_estandar.get_absolute_url(), expected_url)

    def test_tipo_habitacion_precio_formateado(self):
        self.assertEqual(self.tipo_estandar.get_precio_formateado(), "100.00")
        tipo_con_decimales = TipoHabitacion.objects.create(nombre="Test Decimal", capacidad_maxima=1, precio_base_noche=123.45, descripcion_larga="test")
        self.assertEqual(tipo_con_decimales.get_precio_formateado(), "123.45")


    def test_tipo_habitacion_con_amenidades(self):
        self.assertIn(self.amenidad1, self.tipo_estandar.amenidades.all())

class HabitacionModelTestCase(TestCase):
    def setUp(self):
        self.tipo_suite = TipoHabitacion.objects.create(
            nombre="Suite Presidencial",
            descripcion_larga="La mejor suite.",
            capacidad_maxima=4,
            precio_base_noche=500.00
        )
        self.habitacion_101 = Habitacion.objects.create(
            numero="101",
            tipo_habitacion=self.tipo_suite,
            estado='disponible',
            piso="1"
        )

    def test_habitacion_creacion(self):
        self.assertEqual(str(self.habitacion_101), "Habitación N° 101 (Suite Presidencial)")
        self.assertTrue(self.habitacion_101.esta_realmente_disponible)

    def test_habitacion_no_disponible_si_no_para_reserva(self):
        self.habitacion_101.disponible_para_reserva = False
        self.habitacion_101.save()
        self.assertFalse(self.habitacion_101.esta_realmente_disponible)

    def test_habitacion_no_disponible_si_estado_no_es_disponible(self):
        self.habitacion_101.estado = 'mantenimiento'
        self.habitacion_101.save()
        self.assertFalse(self.habitacion_101.esta_realmente_disponible)


class HabitacionViewsTestCase(TestCase):
    def setUp(self):
        self.client_http = Client()
        # Crear configuración del sitio si es necesaria para las vistas (context processor)
        ConfiguracionSitio.objects.create(nombre_hotel="Hotel Pruebas Habitaciones")

        self.amenidad_tv = Amenidad.objects.create(nombre="TV Plana")
        self.tipo_activo = TipoHabitacion.objects.create(
            nombre="Habitación Activa",
            slug="habitacion-activa",
            descripcion_larga="Descripción de la activa.",
            capacidad_maxima=2,
            precio_base_noche=120.00,
            activo=True,
            destacado=True
        )
        self.tipo_activo.amenidades.add(self.amenidad_tv)

        # Crear imagen principal para tipo_activo
        # Necesitarás crear un archivo de imagen dummy para que este test pase si usas ImageField.
        # from django.core.files.uploadedfile import SimpleUploadedFile
        # dummy_image = SimpleUploadedFile("test_img.jpg", b"file_content", content_type="image/jpeg")
        # self.tipo_activo.imagen_principal = dummy_image
        # self.tipo_activo.save()
        # ImagenHabitacion.objects.create(tipo_habitacion=self.tipo_activo, imagen=dummy_image, orden=1)


        self.tipo_inactiva = TipoHabitacion.objects.create(
            nombre="Habitación Inactiva",
            slug="habitacion-inactiva",
            descripcion_larga="No disponible.",
            capacidad_maxima=1,
            precio_base_noche=50.00,
            activo=False # Importante: Inactiva
        )
        self.lista_url = reverse('habitaciones:lista_tipos_habitacion')
        self.detalle_url_activa = reverse('habitaciones:detalle_tipo_habitacion', kwargs={'slug': self.tipo_activo.slug})

    def test_lista_tipos_habitacion_view(self):
        response = self.client_http.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habitaciones/habitacion_list.html')
        self.assertContains(response, self.tipo_activo.nombre)
        self.assertNotContains(response, self.tipo_inactiva.nombre) # No debe mostrar tipos inactivos
        self.assertIn(self.tipo_activo, response.context['tipos_habitacion'])

    def test_detalle_tipo_habitacion_view_activa(self):
        response = self.client_http.get(self.detalle_url_activa)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habitaciones/habitacion_detail.html')
        self.assertEqual(response.context['tipo_habitacion'], self.tipo_activo)
        self.assertContains(response, self.tipo_activo.nombre)
        self.assertContains(response, self.amenidad_tv.nombre) # Verificar que se muestren amenidades

    def test_detalle_tipo_habitacion_view_inactiva_returns_404(self):
        # El queryset en la DetailView (o la lógica en la function view) debe filtrar por activo=True
        detalle_url_inactiva = reverse('habitaciones:detalle_tipo_habitacion', kwargs={'slug': self.tipo_inactiva.slug})
        response = self.client_http.get(detalle_url_inactiva)
        self.assertEqual(response.status_code, 404)

    def test_detalle_tipo_habitacion_view_slug_no_existente_returns_404(self):
        url_no_existente = reverse('habitaciones:detalle_tipo_habitacion', kwargs={'slug': 'slug-que-no-existe'})
        response = self.client_http.get(url_no_existente)
        self.assertEqual(response.status_code, 404)
```
