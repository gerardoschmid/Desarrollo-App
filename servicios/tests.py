# Contenido de servicios/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.text import slugify
from .models import Servicio, CategoriaServicio
from core.models import ConfiguracionSitio # Importar si las vistas lo usan para el contexto global

class CategoriaServicioModelTestCase(TestCase):
    def test_categoria_servicio_creacion(self):
        categoria = CategoriaServicio.objects.create(nombre="Restauración", icono_fa="fas fa-utensils", orden=1)
        self.assertEqual(str(categoria), "Restauración")
        self.assertEqual(categoria.slug, slugify("Restauración"))

class ServicioModelTestCase(TestCase):
    def setUp(self):
        self.categoria_bienestar = CategoriaServicio.objects.create(nombre="Bienestar")
        self.servicio_spa = Servicio.objects.create(
            nombre="Masaje Relajante SPA",
            categoria=self.categoria_bienestar,
            descripcion_larga="Un masaje profundo para aliviar el estrés.",
            descripcion_corta="Masaje anti-estrés.",
            icono_fa="fas fa-spa",
            precio=75.00,
            unidad_precio='evento',
            disponible=True,
            requiere_reserva_previa=True
        )
        self.servicio_wifi = Servicio.objects.create(
            nombre="WiFi de Alta Velocidad",
            descripcion_larga="Conexión a internet en todas las áreas del hotel.",
            precio=None, # Gratuito o incluido
            disponible=True
        )

    def test_servicio_creacion_y_slug(self):
        self.assertEqual(self.servicio_spa.nombre, "Masaje Relajante SPA")
        self.assertEqual(self.servicio_spa.slug, slugify("Masaje Relajante SPA"))
        self.assertEqual(str(self.servicio_spa), "Masaje Relajante SPA")

    def test_servicio_get_absolute_url(self):
        expected_url = reverse('servicios:detalle_servicio', kwargs={'slug': self.servicio_spa.slug})
        self.assertEqual(self.servicio_spa.get_absolute_url(), expected_url)

    def test_servicio_precio_display(self):
        self.assertEqual(self.servicio_spa.get_precio_display_completo(), "$75.00 (Por Evento/Servicio Completo)")
        self.assertEqual(self.servicio_wifi.get_precio_display_completo(), "Consultar")

class ServicioViewsTestCase(TestCase):
    def setUp(self):
        self.client_http = Client()
        ConfiguracionSitio.objects.create(nombre_hotel="Hotel Servicios Test") # Para el context_processor

        self.cat1 = CategoriaServicio.objects.create(nombre="Comida", orden=1)
        self.cat2 = CategoriaServicio.objects.create(nombre="Actividades", orden=0) # Orden menor, aparece primero

        self.servicio_activo1 = Servicio.objects.create(
            nombre="Desayuno Buffet",
            slug="desayuno-buffet",
            categoria=self.cat1,
            descripcion_larga="Variedad de opciones para empezar el día.",
            disponible=True,
            destacado=True
        )
        self.servicio_activo2 = Servicio.objects.create(
            nombre="Clases de Yoga",
            slug="clases-yoga",
            categoria=self.cat2,
            descripcion_larga="Relájate con nuestras clases matutinas.",
            disponible=True
        )
        self.servicio_inactivo = Servicio.objects.create(
            nombre="Cena Especial (No Disponible)",
            slug="cena-especial-no-disponible",
            categoria=self.cat1,
            descripcion_larga="Próximamente.",
            disponible=False # Importante: Inactivo
        )
        self.lista_url = reverse('servicios:lista_servicios')
        self.detalle_url_activo1 = reverse('servicios:detalle_servicio', kwargs={'slug': self.servicio_activo1.slug})

    def test_lista_servicios_view(self):
        response = self.client_http.get(self.lista_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicios/servicio_list.html')

        # Verificar que los servicios activos estén y el inactivo no
        self.assertContains(response, self.servicio_activo1.nombre)
        self.assertContains(response, self.servicio_activo2.nombre)
        self.assertNotContains(response, self.servicio_inactivo.nombre)

        # Verificar el orden por categoría (Actividades tiene orden 0, Comida tiene orden 1)
        # El context['servicios_por_categoria'] debe tener 'Actividades' antes que 'Comida'
        # Esto asume que la vista agrupa por categoría y respeta el orden de la categoría.
        # La vista actual no agrupa, solo lista todos los servicios.
        # Para probar el orden de servicios individuales, necesitaríamos saber el orden exacto esperado.
        # Por ahora, nos aseguramos que los servicios estén en el contexto.
        servicios_en_contexto = response.context['servicios_por_categoria'] # La vista actual usa 'servicios_por_categoria'

        nombres_servicios_en_orden_esperado = [self.servicio_activo2.nombre, self.servicio_activo1.nombre] # Yoga (cat Actividades) antes que Desayuno (cat Comida)

        # Extraer nombres de servicios del contexto para verificar el orden
        # Esto es un poco más complejo porque servicios_por_categoria es un dict
        # {categoria: [servicios_de_esa_cat]}
        # Primero, obtengamos una lista plana de servicios en el orden que aparecen en la plantilla
        # La plantilla itera sobre servicios_por_categoria.items() que está ordenado por Categoria.orden
        # y luego sobre los servicios dentro de cada categoría.

        nombres_servicios_renderizados = []
        for categoria, servicios_lista in servicios_en_contexto:
            for servicio in servicios_lista:
                nombres_servicios_renderizados.append(servicio.nombre)

        # Verificar que los nombres aparezcan en el orden esperado
        # (Yoga debe aparecer antes que Desayuno porque la categoría "Actividades" tiene orden 0)
        if len(nombres_servicios_renderizados) >= 2:
             self.assertLess(nombres_servicios_renderizados.index(self.servicio_activo2.nombre), nombres_servicios_renderizados.index(self.servicio_activo1.nombre))


    def test_detalle_servicio_view_activo(self):
        response = self.client_http.get(self.detalle_url_activo1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'servicios/servicio_detail.html')
        self.assertEqual(response.context['servicio'], self.servicio_activo1)
        self.assertContains(response, self.servicio_activo1.nombre)
        self.assertContains(response, self.servicio_activo1.descripcion_larga)

    def test_detalle_servicio_view_inactivo_returns_404(self):
        detalle_url_inactiva = reverse('servicios:detalle_servicio', kwargs={'slug': self.servicio_inactivo.slug})
        response = self.client_http.get(detalle_url_inactiva)
        # La vista actual filtra por disponible=True, así que un servicio no disponible debería dar 404
        self.assertEqual(response.status_code, 404)

    def test_detalle_servicio_view_slug_no_existente_returns_404(self):
        url_no_existente = reverse('servicios:detalle_servicio', kwargs={'slug': 'slug-que-no-existe-en-absoluto'})
        response = self.client_http.get(url_no_existente)
        self.assertEqual(response.status_code, 404)
```
