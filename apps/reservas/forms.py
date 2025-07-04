from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.habitaciones.models import TipoHabitacion, Habitacion
from apps.clientes.models import Cliente
from .models import Reserva
import datetime

class ReservaPublicForm(forms.ModelForm):
    tipo_habitacion = forms.ModelChoiceField(
        queryset=TipoHabitacion.objects.all(),
        label=_("Tipo de Habitación Preferido"),
        empty_label=_("Seleccione un tipo de habitación"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fecha_entrada = forms.DateField(
        label=_("Fecha de Entrada"),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker', 'placeholder': _('YYYY-MM-DD')})
    )
    fecha_salida = forms.DateField(
        label=_("Fecha de Salida"),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control datepicker', 'placeholder': _('YYYY-MM-DD')})
    )
    numero_adultos = forms.IntegerField(
        label=_("Adultos"),
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1'})
    )
    numero_ninos = forms.IntegerField(
        label=_("Niños (menores de 12 años)"),
        min_value=0,
        initial=0,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )

    # Campos para el cliente (si no está logueado o es nuevo)
    nombre_cliente = forms.CharField(
        label=_("Nombre Completo del Huésped Principal"),
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email_cliente = forms.EmailField(
        label=_("Email de Contacto"),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono_cliente = forms.CharField(
        label=_("Teléfono de Contacto"),
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Reserva
        fields = [
            'tipo_habitacion', 'fecha_entrada', 'fecha_salida',
            'numero_adultos', 'numero_ninos',
            'nombre_cliente', 'email_cliente', 'telefono_cliente',
            'notas_adicionales'
        ]
        widgets = {
            'notas_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('¿Alguna petición especial?')}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # Para acceder al request.user si es necesario
        super().__init__(*args, **kwargs)

        # Si se pasa un tipo_habitacion_id en la URL, preseleccionarlo
        if 'initial' in kwargs and 'tipo_habitacion' in kwargs['initial']:
            self.fields['tipo_habitacion'].initial = kwargs['initial']['tipo_habitacion']
        elif self.request and self.request.GET.get('tipo_habitacion'):
            try:
                tipo_id = int(self.request.GET.get('tipo_habitacion'))
                self.fields['tipo_habitacion'].initial = TipoHabitacion.objects.get(pk=tipo_id)
            except (ValueError, TipoHabitacion.DoesNotExist):
                pass

        # Si se pasan fechas en la URL, preseleccionarlas
        if self.request:
            if self.request.GET.get('fecha_entrada'):
                self.fields['fecha_entrada'].initial = self.request.GET.get('fecha_entrada')
            if self.request.GET.get('fecha_salida'):
                self.fields['fecha_salida'].initial = self.request.GET.get('fecha_salida')


    def clean_fecha_entrada(self):
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        if fecha_entrada and fecha_entrada < timezone.now().date():
            # Permitir si es para hoy, pero no pasado.
            # Si se quisiera permitir edición de reservas pasadas (no es el caso de este form público)
            # esta validación cambiaría.
            if fecha_entrada < datetime.date.today(): # Estricto: no hoy si ya pasó la hora de check-in, etc.
                 raise ValidationError(_("La fecha de entrada no puede ser en el pasado."), code='fecha_pasada')
        return fecha_entrada

    def clean_fecha_salida(self):
        fecha_entrada = self.cleaned_data.get('fecha_entrada')
        fecha_salida = self.cleaned_data.get('fecha_salida')
        if fecha_entrada and fecha_salida:
            if fecha_salida <= fecha_entrada:
                raise ValidationError(_("La fecha de salida debe ser posterior a la fecha de entrada."), code='fecha_salida_invalida')
            if (fecha_salida - fecha_entrada).days > 90: # Límite de ejemplo: 90 días
                raise ValidationError(_("La estancia no puede exceder los 90 días."), code='estancia_muy_larga')
        return fecha_salida

    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        tipo_habitacion = cleaned_data.get('tipo_habitacion')
        numero_adultos = cleaned_data.get('numero_adultos', 0)
        numero_ninos = cleaned_data.get('numero_ninos', 0)
        total_huespedes = numero_adultos + numero_ninos

        if not tipo_habitacion: # Si no se seleccionó tipo, no podemos validar capacidad
            # Esto debería ser capturado por la validación de campo requerido, pero por si acaso.
            # self.add_error('tipo_habitacion', _("Debe seleccionar un tipo de habitación."))
            return cleaned_data

        # Validar capacidad
        # Asumimos que todas las habitaciones de un mismo tipo tienen la misma capacidad base.
        # Si la capacidad varía por habitación individual dentro de un tipo, esta lógica debe ser más compleja.
        # Por ahora, tomamos la capacidad de la primera habitación de ese tipo como referencia,
        # o podríamos añadir un campo 'capacidad_maxima' al modelo TipoHabitacion.

        # Buscamos una habitación de referencia para la capacidad.
        # Esto es una simplificación. Idealmente, TipoHabitacion tendría su propia capacidad.
        habitacion_referencia = Habitacion.objects.filter(tipo_habitacion=tipo_habitacion).first()
        if habitacion_referencia:
            capacidad_maxima_tipo = habitacion_referencia.capacidad
            if total_huespedes > capacidad_maxima_tipo:
                self.add_error(None, ValidationError(
                    _("El número total de huéspedes (%(total_huespedes)s) excede la capacidad máxima (%(capacidad)s) para el tipo de habitación '%(tipo)s'.") %
                    {'total_huespedes': total_huespedes, 'capacidad': capacidad_maxima_tipo, 'tipo': tipo_habitacion.nombre},
                    code='excede_capacidad'
                ))
        else:
            # No hay habitaciones de este tipo, lo cual es un problema de datos o configuración
            self.add_error('tipo_habitacion', _("No hay habitaciones configuradas para este tipo. Contacte al administrador."))
            return cleaned_data


        # Validación de disponibilidad en tiempo real (se llamará desde la vista con AJAX,
        # pero también es bueno tener una validación final aquí).
        # Esta validación buscará CUALQUIER habitación disponible de ese TIPO.
        if fecha_entrada and fecha_salida and tipo_habitacion:
            # Obtener todas las habitaciones del tipo seleccionado
            habitaciones_del_tipo = Habitacion.objects.filter(tipo_habitacion=tipo_habitacion, disponible=True)

            habitacion_disponible_encontrada = False
            for habitacion_potencial in habitaciones_del_tipo:
                if total_huespedes > habitacion_potencial.capacidad: # Verificar capacidad de esta habitación específica
                    continue

                reservas_solapadas = Reserva.objects.filter(
                    habitacion=habitacion_potencial,
                    estado__in=[Reserva.ESTADO_CONFIRMADA, Reserva.ESTADO_PENDIENTE]
                ).filter(
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                )
                if not reservas_solapadas.exists():
                    habitacion_disponible_encontrada = True
                    cleaned_data['habitacion_asignada_id'] = habitacion_potencial.id # Guardamos la ID para la vista
                    break # Encontramos una, salimos del bucle

            if not habitacion_disponible_encontrada:
                self.add_error(None, ValidationError(
                    _("Lo sentimos, no hay habitaciones del tipo '%(tipo)s' disponibles para las fechas y número de huéspedes seleccionados.") %
                    {'tipo': tipo_habitacion.nombre},
                    code='no_disponible'
                ))

        return cleaned_data
