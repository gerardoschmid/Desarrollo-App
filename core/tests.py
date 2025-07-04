# Contenido de core/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import ConfiguracionSitio, MensajeContacto, ImagenGaleria
from .forms import ContactoForm

class CoreViewsTestCase(TestCase):
    def setUp(self):
        # Es buena práctica crear una configuración si tus vistas dependen de ella
        self.config = ConfiguracionSitio.objects.create(nombre_hotel="Hotel Test")
        self.client = Client()

    def test_index_view_status_code(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')
        self.assertContains(response, self.config.nombre_hotel)

    def test_about_view_status_code(self):
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/about.html')
        self.assertContains(response, "Sobre Nosotros")

    def test_contact_view_get_status_code_and_form(self):
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/contacto.html')
        self.assertIsInstance(response.context['form'], ContactoForm)
        self.assertContains(response, "Ponte en Contacto")

    def test_gallery_view_status_code(self):
        ImagenGaleria.objects.create(titulo="Imagen 1", imagen="galeria_hotel/test1.jpg") # Asume que tienes una imagen de prueba
        ImagenGaleria.objects.create(titulo="Imagen 2", imagen="galeria_hotel/test2.jpg")
        response = self.client.get(reverse('core:gallery'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/gallery.html')
        self.assertContains(response, "Galería")
        self.assertEqual(len(response.context['imagenes']), 2)


class ContactFormTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('core:contact')
        ConfiguracionSitio.objects.create(nombre_hotel="Hotel Contacto Test")


    def test_valid_contact_form_submission(self):
        form_data = {
            'nombre': 'Test User',
            'email': 'test@example.com',
            'asunto': 'Test Subject for Contact',
            'mensaje': 'This is a test message for the contact form.'
        }
        response = self.client.post(self.contact_url, data=form_data)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito
        self.assertRedirects(response, self.contact_url)

        # Verificar que el mensaje se guardó
        self.assertTrue(MensajeContacto.objects.filter(email='test@example.com', asunto='Test Subject for Contact').exists())

        # Verificar que se muestra un mensaje de éxito (si usas Django messages framework)
        # Para esto, necesitarías seguir la redirección y verificar el contenido
        response_redirected = self.client.get(self.contact_url)
        self.assertContains(response_redirected, "¡Gracias por tu mensaje!")


    def test_invalid_contact_form_submission_empty_fields(self):
        form_data = {} # Datos vacíos
        response = self.client.post(self.contact_url, data=form_data)
        self.assertEqual(response.status_code, 200) # Debería volver a mostrar el formulario con errores
        self.assertFormError(response, 'form', 'nombre', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'email', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'asunto', 'Este campo es obligatorio.')
        self.assertFormError(response, 'form', 'mensaje', 'Este campo es obligatorio.')
        self.assertContains(response, "Hubo un error en el formulario") # Mensaje de error general

    def test_invalid_contact_form_submission_invalid_email(self):
        form_data = {
            'nombre': 'Test User',
            'email': 'notanemail', # Email inválido
            'asunto': 'Test Subject',
            'mensaje': 'This is a test message.'
        }
        response = self.client.post(self.contact_url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', 'Introduzca una dirección de correo electrónico válida.')


class ConfiguracionSitioModelTestCase(TestCase):
    def test_crear_configuracion(self):
        config = ConfiguracionSitio.objects.create(
            nombre_hotel="Mi Hotel de Prueba",
            email_contacto="contacto@mihotelprueba.com"
        )
        self.assertEqual(str(config), "Configuración de Mi Hotel de Prueba")
        self.assertEqual(ConfiguracionSitio.objects.count(), 1)

    def test_singleton_configuracion(self):
        from django.core.exceptions import ValidationError
        ConfiguracionSitio.objects.create(nombre_hotel="Config 1")
        with self.assertRaises(ValidationError): # El modelo ahora previene esto en save()
            ConfiguracionSitio.objects.create(nombre_hotel="Config 2")
        self.assertEqual(ConfiguracionSitio.objects.count(), 1)

class ContextProcessorsTestCase(TestCase):
    def test_site_config_context_processor(self):
        # Primero, asegúrate de que exista una configuración
        config = ConfiguracionSitio.objects.create(nombre_hotel="Hotel Global Test")

        # Haz una solicitud a una página que use el base.html (y por ende el context processor)
        response = self.client.get(reverse('core:index'))

        self.assertEqual(response.status_code, 200)
        # Verifica que 'config' esté en el contexto y sea la instancia correcta
        self.assertIn('config', response.context)
        self.assertEqual(response.context['config'], config)
        self.assertEqual(response.context['config'].nombre_hotel, "Hotel Global Test")

    def test_site_config_context_processor_no_config(self):
        # Si no hay configuración, el context processor debería devolver None o un objeto por defecto
        # dependiendo de su implementación. Aquí asumimos que devuelve None si no hay config.
        # Asegurarse que no haya ConfiguracionSitio
        ConfiguracionSitio.objects.all().delete()

        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200) # La vista debe manejar esto graciosamente
        self.assertIn('config', response.context)
        # Si get_site_config() devuelve None cuando no hay objetos:
        self.assertIsNone(response.context['config'])
        # O si devuelve un objeto por defecto, testea eso.
        # Por ejemplo, si tu context processor crea uno por defecto:
        # self.assertIsNotNone(response.context['config'])
        # self.assertEqual(response.context['config'].nombre_hotel, "Hotel Premium MVP") # Valor por defecto del modelo
        # Nota: La implementación actual de get_site_config() en views.py y el context_processor
        # devolverá None si no hay configuración. Las plantillas usan `config.nombre_hotel|default:'...'`
        # para manejar esto.
```
