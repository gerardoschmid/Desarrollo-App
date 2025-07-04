# Contenido de clientes/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Cliente
from reservas.models import Reserva, TipoHabitacion # Para probar el historial de reservas
import datetime
from django.utils import timezone

class ClienteModelTestCase(TestCase):
    def setUp(self):
        self.cliente1 = Cliente.objects.create(
            nombre_completo="Juan Alberto Pérez García",
            email="juan.perez.garcia@example.com",
            telefono="1234567890"
        )
        self.cliente2 = Cliente.objects.create(
            nombre_completo="Ana María Gómez López",
            email="ana.gomez.lopez@example.com"
        )
        self.tipo_hab_test = TipoHabitacion.objects.create(
            nombre="Sencilla Test",
            capacidad_maxima=1,
            precio_base_noche=50.00,
            descripcion_larga="Para tests"
        )

    def test_cliente_creacion_correcta(self):
        self.assertEqual(self.cliente1.nombre_completo, "Juan Alberto Pérez García")
        self.assertEqual(self.cliente1.email, "juan.perez.garcia@example.com")
        self.assertEqual(str(self.cliente1), "Juan Alberto Pérez García (juan.perez.garcia@example.com)")

    def test_cliente_email_debe_ser_unico(self):
        from django.db.utils import IntegrityError
        with self.assertRaises(IntegrityError): # Error a nivel de BD por `unique=True`
            Cliente.objects.create(
                nombre_completo="Otro Juan Pérez",
                email="juan.perez.garcia@example.com" # Email repetido
            )

    def test_tipo_y_numero_documento_unico_validacion(self):
        Cliente.objects.create(
            nombre_completo="Cliente Documentado",
            email="doc1@example.com",
            tipo_documento='DNI',
            numero_documento='12345678A'
        )
        cliente_duplicado_doc = Cliente(
            nombre_completo="Otro Cliente Documentado",
            email="doc2@example.com",
            tipo_documento='DNI',
            numero_documento='12345678A' # Mismo tipo y número
        )
        with self.assertRaises(ValidationError) as context:
            cliente_duplicado_doc.full_clean() # full_clean() llama al método clean() del modelo

        self.assertIn('numero_documento', context.exception.message_dict)
        self.assertIn("Ya existe un cliente con este tipo y número de documento", context.exception.message_dict['numero_documento'][0])

        # Probar que se puede guardar si el número es diferente
        cliente_doc_diferente = Cliente(
            nombre_completo="Cliente Doc Dif",
            email="doc3@example.com",
            tipo_documento='DNI',
            numero_documento='98765432B'
        )
        try:
            cliente_doc_diferente.full_clean()
            cliente_doc_diferente.save()
        except ValidationError:
            self.fail("No debería fallar la validación con documento diferente.")


    def test_cantidad_reservas_realizadas_property(self):
        self.assertEqual(self.cliente1.cantidad_reservas_realizadas, 0)

        # Crear una reserva para cliente1
        Reserva.objects.create(
            cliente=self.cliente1, # Asegúrate que el related_name en Reserva es 'reservas_cliente' o ajusta aquí
            tipo_habitacion_solicitada=self.tipo_hab_test,
            fecha_llegada=timezone.now().date() + datetime.timedelta(days=1),
            fecha_salida=timezone.now().date() + datetime.timedelta(days=3),
            numero_huespedes_adultos=1
        )
        self.assertEqual(self.cliente1.cantidad_reservas_realizadas, 1)
        self.assertEqual(self.cliente2.cantidad_reservas_realizadas, 0)

    def test_ultima_reserva_fecha_property(self):
        self.assertIsNone(self.cliente2.ultima_reserva_fecha)

        # Crear reservas con fechas de creación específicas
        # Para controlar la fecha_creacion (auto_now_add=True), necesitamos "engañar" un poco
        # o crear y luego actualizar (lo cual es más complejo para auto_now_add).
        # Una forma es crear, luego buscar y actualizar si el ORM lo permite sin re-triggering auto_now_add.

        fecha_reserva_antigua = timezone.now() - datetime.timedelta(days=10)
        fecha_reserva_reciente = timezone.now() - datetime.timedelta(days=2)

        res1 = Reserva.objects.create(
            cliente=self.cliente1, tipo_habitacion_solicitada=self.tipo_hab_test,
            fecha_llegada=timezone.now().date() + datetime.timedelta(days=10),
            fecha_salida=timezone.now().date() + datetime.timedelta(days=12),
            numero_huespedes_adultos=1
        )
        # Forzar la fecha de creación (esto es para testing, no es una práctica común en código de producción)
        Reserva.objects.filter(pk=res1.pk).update(fecha_creacion=fecha_reserva_antigua)
        res1.refresh_from_db() # Actualizar el objeto en memoria

        res2 = Reserva.objects.create(
            cliente=self.cliente1, tipo_habitacion_solicitada=self.tipo_hab_test,
            fecha_llegada=timezone.now().date() + datetime.timedelta(days=20),
            fecha_salida=timezone.now().date() + datetime.timedelta(days=22),
            numero_huespedes_adultos=1
        )
        Reserva.objects.filter(pk=res2.pk).update(fecha_creacion=fecha_reserva_reciente)
        res2.refresh_from_db()

        # Comprobar que la fecha de la última reserva sea la más reciente (comparando solo la parte de la fecha)
        self.assertIsNotNone(self.cliente1.ultima_reserva_fecha)
        self.assertEqual(self.cliente1.ultima_reserva_fecha.date(), fecha_reserva_reciente.date())
```
