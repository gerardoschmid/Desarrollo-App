from django.views.generic import TemplateView
from django.shortcuts import render # , redirect
# from django.core.mail import send_mail
# from django.conf import settings
# from .forms import ContactoForm # Crearíamos un forms.py en core para esto
from apps.servicios.models import Servicio # Para mostrar en la página de inicio
from apps.habitaciones.models import TipoHabitacion # Para mostrar en la página de inicio o galería

class HomePageView(TemplateView):
    template_name = "core/inicio.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['servicios_destacados'] = Servicio.objects.filter(disponible=True, imagen__isnull=False)[:4] # Ejemplo: 4 servicios con imagen
        context['tipos_habitacion_destacados'] = TipoHabitacion.objects.all()[:3] # Ejemplo: 3 tipos de habitación
        context['page_title'] = "Bienvenido a Hotel Premium" # Título para la plantilla base
        # Aquí podrías añadir un formulario de búsqueda de disponibilidad si lo deseas
        return context

class SobreNosotrosPageView(TemplateView):
    template_name = "core/sobre_nosotros.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Sobre Nosotros"
        return context

class GaleriaPageView(TemplateView):
    template_name = "core/galeria.html"
    # Esta vista podría necesitar más lógica para obtener imágenes de diferentes fuentes (habitaciones, instalaciones generales)
    # Por ahora, asumimos que el template manejará la muestra de imágenes estáticas o de un contexto simple.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Galería de Imágenes"
        # Ejemplo: podrías pasar aquí todas las imágenes de habitaciones
        # from apps.habitaciones.models import ImagenHabitacion
        # context['imagenes_galeria'] = ImagenHabitacion.objects.all()
        return context

class ContactoPageView(TemplateView): # Podría ser FormView si se usa un Django Form
    template_name = "core/contacto.html"
    # form_class = ContactoForm # Si se usa FormView
    # success_url = reverse_lazy('core:contacto_enviado') # Una página de "mensaje enviado"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Contacto"
        # context['form'] = self.form_class() # Si no es FormView pero quieres pasar el form manualmente
        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         # Lógica para enviar email
    #         nombre = form.cleaned_data['nombre']
    #         email_origen = form.cleaned_data['email']
    #         mensaje = form.cleaned_data['mensaje']
    #         try:
    #             send_mail(
    #                 f"Mensaje de contacto de {nombre} ({email_origen})",
    #                 mensaje,
    #                 settings.DEFAULT_FROM_EMAIL, # O email_origen si quieres responder directamente
    #                 [settings.EMAIL_HOST_USER], # Email del administrador del hotel
    #                 fail_silently=False,
    #             )
    #             # Redirigir a una página de éxito o mostrar mensaje
    #             return redirect(self.success_url)
    #         except Exception as e:
    #             # Manejar error de envío
    #             form.add_error(None, f"Error al enviar el mensaje: {e}")
    #     return render(request, self.template_name, {'form': form, 'page_title': "Contacto"})

# class ContactoEnviadoView(TemplateView):
#    template_name = "core/contacto_enviado.html"
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['page_title'] = "Mensaje Enviado"
#        return context

# Si se usa una función para el envío del formulario de contacto:
# def enviar_mensaje_contacto(request):
#     if request.method == 'POST':
#         form = ContactoForm(request.POST)
#         if form.is_valid():
#             # Lógica de envío de email como arriba
#             # ...
#             return redirect('core:contacto_enviado') # O alguna confirmación
#     else:
#         form = ContactoForm()
#     return render(request, 'core/contacto_form_snippet.html', {'form': form}) # Un snippet o la página completa
