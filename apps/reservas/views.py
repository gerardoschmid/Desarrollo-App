from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import Reserva, Habitacion, Cliente
from .forms import ReservaPublicForm # Importar el nuevo formulario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
import datetime

# Vista pública para crear una reserva (podría empezar con un formulario de búsqueda)
# class disponibilidad_y_reserva(FormView) o una vista basada en función más compleja.
# Por ahora, una CreateView simple para el formulario de reserva directo.
# class CrearReservaView(CreateView): # Esta es una versión simplificada
#     model = Reserva
#     form_class = ReservaForm # Necesitará un formulario que permita seleccionar habitación, fechas, etc.
#     template_name = 'reservas/reserva_form_public.html' # Template para el público
#     success_url = reverse_lazy('reservas:confirmacion_reserva') # Necesita pasar el pk

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = "Realizar una Reserva"
#         # Aquí podríamos pasar información de habitaciones disponibles si el proceso es más guiado
#         return context

#     def form_valid(self, form):
#         # Aquí se puede añadir lógica para verificar disponibilidad antes de guardar,
#         # aunque parte de esto ya está en el clean() del modelo.
#         # También se podría crear un Cliente si no existe, o asociarlo si ya existe.
#         # form.instance.cliente = self.request.user.cliente # Si el usuario está logueado y tiene perfil cliente
#         # reserva = form.save()
#         # self.pk_reserva = reserva.pk
#         # messages.success(self.request, "Reserva realizada con éxito. Pendiente de confirmación.")
#         # return super().form_valid(form)
#         # Para pasar el pk a la URL de éxito:
#         # return redirect(reverse('reservas:confirmacion_reserva', kwargs={'pk': self.object.pk}))
#         # Este es un CreateView, el self.object se setea después de form_valid.
#         # Una mejor forma es:
#         self.object = form.save()
#         return redirect(self.get_success_url())


#     def get_success_url(self):
#          return reverse('reservas:confirmacion_reserva', kwargs={'pk': self.object.pk})


# Vista más elaborada para creación de reserva (simulando un proceso)
class CrearReservaView(FormView): # O podría ser una View normal y manejar GET/POST
    # form_class = BusquedaDisponibilidadForm # Primer paso: buscar disponibilidad
    template_name = 'reservas/crear_reserva_paso1.html' # Template para buscar fechas y tipo
    # success_url = reverse_lazy('reservas:crear_reserva_paso2') # URL para el siguiente paso

    # def form_valid(self, form):
    #     # Guardar datos de búsqueda en sesión y redirigir al paso 2
    #     self.request.session['busqueda_reserva'] = form.cleaned_data
    #     return super().form_valid(form)

    # Esta es una implementación más directa para el MVP, usando un form simple para Reserva
    form_class = ReservaPublicForm
    template_name = 'reservas/reserva_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request # Pasar el request al form
        # Pasar 'initial' data si viene de la URL (ej. tipo_habitacion_id)
        initial = kwargs.get('initial', {})
        tipo_habitacion_id = self.request.GET.get('tipo_habitacion')
        if tipo_habitacion_id:
            try:
                initial['tipo_habitacion'] = TipoHabitacion.objects.get(pk=tipo_habitacion_id)
            except (ValueError, TipoHabitacion.DoesNotExist):
                pass # El form manejará si no se encuentra o es inválido

        fecha_entrada = self.request.GET.get('fecha_entrada')
        if fecha_entrada:
            initial['fecha_entrada'] = fecha_entrada

        fecha_salida = self.request.GET.get('fecha_salida')
        if fecha_salida:
            initial['fecha_salida'] = fecha_salida

        kwargs['initial'] = initial
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _("Realizar una Reserva")
        context['form_title'] = _("Complete los datos de su reserva")
        context['submit_button_text'] = _("Solicitar Reserva")
        return context

    def form_valid(self, form):
        # Crear o obtener cliente
        nombre_cliente = form.cleaned_data['nombre_cliente']
        email_cliente = form.cleaned_data['email_cliente']
        telefono_cliente = form.cleaned_data['telefono_cliente']

        # Dividir nombre completo en nombre y apellidos (simple split)
        partes_nombre = nombre_cliente.split(' ', 1)
        nombre = partes_nombre[0]
        apellidos = partes_nombre[1] if len(partes_nombre) > 1 else ''


        cliente, created = Cliente.objects.get_or_create(
            email=email_cliente,
            defaults={'nombre': nombre, 'apellidos': apellidos, 'telefono': telefono_cliente}
        )
        if not created: # Si el cliente ya existía, actualizamos nombre y teléfono si es necesario
            cliente.nombre = nombre
            cliente.apellidos = apellidos
            cliente.telefono = telefono_cliente
            cliente.save()

        # El form ya validó la disponibilidad y guardó 'habitacion_asignada_id' en cleaned_data
        habitacion_asignada_id = form.cleaned_data.get('habitacion_asignada_id')
        if not habitacion_asignada_id:
            # Esto no debería ocurrir si la validación del form es correcta
            messages.error(self.request, _("No se pudo asignar una habitación. Por favor, intente de nuevo."))
            return self.form_invalid(form)

        try:
            habitacion_asignada = Habitacion.objects.get(pk=habitacion_asignada_id)
        except Habitacion.DoesNotExist:
            messages.error(self.request, _("La habitación seleccionada ya no está disponible. Por favor, intente de nuevo."))
            return self.form_invalid(form)

        # Crear la reserva
        reserva = Reserva(
            cliente=cliente,
            habitacion=habitacion_asignada,
            fecha_entrada=form.cleaned_data['fecha_entrada'],
            fecha_salida=form.cleaned_data['fecha_salida'],
            numero_huespedes=form.cleaned_data['numero_adultos'] + form.cleaned_data['numero_ninos'],
            notas_adicionales=form.cleaned_data.get('notas_adicionales', ''),
            estado=Reserva.ESTADO_PENDIENTE # Nueva reserva siempre pendiente
        )
        # El costo total se calcula en el save() del modelo Reserva

        try:
            reserva.full_clean() # Validar el modelo completo antes de guardar
            reserva.save()
            self.object = reserva # Guardar el objeto para get_success_url
            messages.success(self.request, _("Su solicitud de reserva ha sido enviada. Nos pondremos en contacto para confirmar."))
            return redirect(self.get_success_url())
        except ValidationError as e:
            # Convertir errores del modelo a errores del formulario si es posible
            # o mostrar como error no de campo.
            non_field_errors = []
            if hasattr(e, 'error_dict'):
                for field, errors in e.error_dict.items():
                    for error in errors:
                        if field == '__all__':
                            non_field_errors.append(error.message)
                        else:
                            form.add_error(field, error.message)
            else: # error_list
                 for error in e.error_list:
                     non_field_errors.append(error.message)

            if non_field_errors:
                form.add_error(None, ValidationError(non_field_errors))

            return self.form_invalid(form)


    def get_success_url(self):
        return reverse('reservas:confirmacion_reserva', kwargs={'pk': self.object.pk})


class ConfirmacionReservaView(DetailView):
    model = Reserva
    template_name = 'reservas/confirmacion_reserva.html'
    context_object_name = 'reserva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Confirmación de Solicitud de Reserva"
        if self.object:
             context['page_title'] = f"Detalle de Solicitud de Reserva #{self.object.pk}"
        return context

# Vistas de Gestión para Reservas (CRUD)
# class ReservaListView(LoginRequiredMixin, ListView):
class ReservaListView(ListView):
    model = Reserva
    template_name = 'reservas/admin_lista_reservas.html'
    context_object_name = 'reservas'
    # paginate_by = 10
    ordering = ['-fecha_entrada', '-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestión de Reservas"
        return context

# class ReservaDetailView(LoginRequiredMixin, DetailView):
class ReservaDetailView(DetailView):
    model = Reserva
    template_name = 'reservas/admin_detalle_reserva.html'
    context_object_name = 'reserva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Reserva #{self.object.pk}" if self.object else "Detalle de Reserva"
        return context

# class ReservaCreateView(LoginRequiredMixin, CreateView): # Para personal de hotel
class ReservaCreateView(CreateView):
    model = Reserva
    template_name = 'reservas/reserva_form.html' # Puede ser el mismo form que el público o uno específico
    fields = ['habitacion', 'cliente', 'fecha_entrada', 'fecha_salida', 'numero_huespedes', 'estado', 'costo_total', 'notas_adicionales']
    # form_class = ReservaAdminForm
    success_url = reverse_lazy('reservas:admin_lista_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Crear Nueva Reserva (Admin)"
        context['form_title'] = "Registrar Nueva Reserva"
        context['submit_button_text'] = "Guardar Reserva"
        return context

# class ReservaUpdateView(LoginRequiredMixin, UpdateView):
class ReservaUpdateView(UpdateView):
    model = Reserva
    template_name = 'reservas/reserva_form.html'
    fields = ['habitacion', 'cliente', 'fecha_entrada', 'fecha_salida', 'numero_huespedes', 'estado', 'costo_total', 'notas_adicionales']
    # form_class = ReservaAdminForm
    success_url = reverse_lazy('reservas:admin_lista_reservas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editar Reserva #{self.object.pk}" if self.object else "Editar Reserva"
        context['form_title'] = f"Editando Reserva #{self.object.pk}" if self.object else "Editar Reserva"
        context['submit_button_text'] = "Actualizar Reserva"
        return context

# class CancelarReservaView(LoginRequiredMixin, UpdateView): # O una vista específica
class CancelarReservaView(UpdateView):
    model = Reserva
    fields = ['estado'] # Solo permite cambiar el estado
    template_name = 'reservas/reserva_cancelar_form.html' # Un template específico para confirmar cancelación
    success_url = reverse_lazy('reservas:admin_lista_reservas')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Forzar el estado a cancelada o permitir seleccionar solo ese
        # form.fields['estado'].initial = Reserva.ESTADO_CANCELADA
        # form.fields['estado'].widget = forms.HiddenInput() # Si se fuerza
        return form

    def form_valid(self, form):
        if not self.request.user.is_staff: # Medida de seguridad simple
            messages.error(self.request, "No tiene permisos para esta acción.")
            return redirect('core:inicio') # O a donde corresponda

        self.object.estado = Reserva.ESTADO_CANCELADA
        self.object.save()
        messages.success(self.request, f"Reserva #{self.object.pk} ha sido cancelada.")
        # Aquí se podría añadir lógica para liberar la habitación, notificar al cliente, etc.
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Cancelar Reserva #{self.object.pk}" if self.object else "Cancelar Reserva"
        context['reserva'] = self.object
        return context


# class ReservaDeleteView(LoginRequiredMixin, DeleteView):
class ReservaDeleteView(DeleteView):
    model = Reserva
    template_name = 'reservas/reserva_confirm_delete.html'
    success_url = reverse_lazy('reservas:admin_lista_reservas')
    context_object_name = 'reserva'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar Reserva #{self.object.pk}" if self.object else "Eliminar Reserva"
        return context

# API para verificar disponibilidad (ejemplo muy básico)
def verificar_disponibilidad_api(request):
    fecha_entrada_str = request.GET.get('fecha_entrada')
    fecha_salida_str = request.GET.get('fecha_salida')
    tipo_habitacion_id_str = request.GET.get('tipo_habitacion_id')
    num_adultos_str = request.GET.get('numero_adultos', '1')
    num_ninos_str = request.GET.get('numero_ninos', '0')
    reserva_id_str = request.GET.get('reserva_id', None) # Para excluir la reserva actual al editar

    if not all([fecha_entrada_str, fecha_salida_str, tipo_habitacion_id_str]):
        return JsonResponse({'error': _('Parámetros incompletos para verificar disponibilidad.')}, status=400)

    try:
        fecha_entrada = datetime.datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
        fecha_salida = datetime.datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
        tipo_habitacion_id = int(tipo_habitacion_id_str)
        num_adultos = int(num_adultos_str)
        num_ninos = int(num_ninos_str)
        total_huespedes = num_adultos + num_ninos
        tipo_habitacion = TipoHabitacion.objects.get(id=tipo_habitacion_id)
    except (ValueError, TypeError, TipoHabitacion.DoesNotExist):
        return JsonResponse({'error': _('Parámetros inválidos o tipo de habitación no encontrado.')}, status=400)

    if fecha_salida <= fecha_entrada:
        return JsonResponse({'disponible': False, 'mensaje': _('La fecha de salida debe ser posterior a la fecha de entrada.')})

    if fecha_entrada < datetime.date.today():
        return JsonResponse({'disponible': False, 'mensaje': _('La fecha de entrada no puede ser en el pasado.')})

    # Lógica de verificación de disponibilidad para el tipo de habitación
    habitaciones_del_tipo = Habitacion.objects.filter(tipo_habitacion=tipo_habitacion, disponible=True)

    habitacion_disponible_encontrada = False
    for habitacion_potencial in habitaciones_del_tipo:
        if total_huespedes > habitacion_potencial.capacidad:
            continue # Esta habitación no tiene suficiente capacidad

        query_reservas_solapadas = Reserva.objects.filter(
            habitacion=habitacion_potencial,
            estado__in=[Reserva.ESTADO_CONFIRMADA, Reserva.ESTADO_PENDIENTE]
        ).filter(
            fecha_entrada__lt=fecha_salida,
            fecha_salida__gt=fecha_entrada
        )
        # Si estamos verificando para una reserva existente (ej. al editar), la excluimos
        if reserva_id_str:
            try:
                reserva_id = int(reserva_id_str)
                query_reservas_solapadas = query_reservas_solapadas.exclude(pk=reserva_id)
            except ValueError:
                pass # ID de reserva inválido, no excluir nada

        if not query_reservas_solapadas.exists():
            habitacion_disponible_encontrada = True
            break

    if habitacion_disponible_encontrada:
        return JsonResponse({
            'disponible': True,
            'mensaje': _("Tipo de habitación disponible para las fechas y huéspedes seleccionados.")
        })
    else:
        return JsonResponse({
            'disponible': False,
            'mensaje': _("Lo sentimos, no hay habitaciones del tipo '%(tipo)s' disponibles para las fechas y número de huéspedes seleccionados.") % {'tipo': tipo_habitacion.nombre}
        })

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError # Asegúrate de importarla si la usas en form_valid
from apps.habitaciones.models import TipoHabitacion # Asegurar que esté importado si se usa en get_form_kwargs
# from django import forms # Para el widget HiddenInput en CancelarReservaView
# (Asegúrate de tener todas las importaciones necesarias al inicio del archivo)
