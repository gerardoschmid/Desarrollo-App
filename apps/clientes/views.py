from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Cliente
# from .forms import ClienteForm # Si se necesita un formulario personalizado
from django.contrib.auth.mixins import LoginRequiredMixin # Para proteger vistas de gestión

# Vistas de Gestión para Clientes (CRUD)
# Todas estas vistas deberían ser accesibles solo por personal autorizado.
# Se añade LoginRequiredMixin como ejemplo, pero podría ser PermissionRequiredMixin.

# class ClienteListView(LoginRequiredMixin, ListView):
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/admin_lista_clientes.html'
    context_object_name = 'clientes'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestión de Clientes"
        return context

# class ClienteDetailView(LoginRequiredMixin, DetailView):
class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/admin_detalle_cliente.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Cliente: {self.object.nombre_completo}" if self.object else "Detalle de Cliente"
        # Aquí podríamos añadir el historial de reservas del cliente
        # from apps.reservas.models import Reserva
        # context['historial_reservas'] = Reserva.objects.filter(cliente=self.object).order_by('-fecha_entrada')
        return context

# class ClienteCreateView(LoginRequiredMixin, CreateView):
class ClienteCreateView(CreateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'apellidos', 'email', 'telefono'] # O usar form_class
    # form_class = ClienteForm
    success_url = reverse_lazy('clientes:admin_lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Registrar Nuevo Cliente"
        context['form_title'] = "Datos del Nuevo Cliente"
        context['submit_button_text'] = "Guardar Cliente"
        return context

# class ClienteUpdateView(LoginRequiredMixin, UpdateView):
class ClienteUpdateView(UpdateView):
    model = Cliente
    template_name = 'clientes/cliente_form.html'
    fields = ['nombre', 'apellidos', 'email', 'telefono']
    # form_class = ClienteForm
    success_url = reverse_lazy('clientes:admin_lista_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editar Cliente: {self.object.nombre_completo}" if self.object else "Editar Cliente"
        context['form_title'] = f"Editando Cliente: {self.object.nombre_completo}" if self.object else "Editar Cliente"
        context['submit_button_text'] = "Actualizar Cliente"
        return context

# class ClienteDeleteView(LoginRequiredMixin, DeleteView):
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:admin_lista_clientes')
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar Cliente: {self.object.nombre_completo}" if self.object else "Eliminar Cliente"
        return context

# Vistas para el perfil del cliente (si se implementa registro y login de clientes)
# class PerfilClienteView(LoginRequiredMixin, DetailView):
#     model = Cliente
#     template_name = 'clientes/perfil_cliente.html'
#     context_object_name = 'cliente'
#     def get_object(self):
#         # Asumiendo que el cliente está ligado al usuario logueado
#         # o se busca por un ID específico si es un admin viendo un perfil.
#         # Esto necesita una lógica más robusta dependiendo de cómo se asocie Cliente con User.
#         # Por ejemplo, si Cliente tiene un OneToOneField 'user' con el modelo User de Django:
#         # return Cliente.objects.get(user=self.request.user)
#         # O si es un admin, se podría pasar el pk por la URL.
#         # Para este ejemplo, asumimos que se accede a través de un pk en la URL.
#         return super().get_object()

# class EditarPerfilClienteView(LoginRequiredMixin, UpdateView):
#      model = Cliente
#      template_name = 'clientes/editar_perfil_cliente.html'
#      fields = ['nombre', 'apellidos', 'telefono'] # Email usualmente no se cambia o requiere verificación
#      # success_url = reverse_lazy('clientes:perfil_cliente')
#      def get_object(self):
#          # return Cliente.objects.get(user=self.request.user)
#          return super().get_object() # Si se usa pk

# class RegistroClienteView(CreateView):
#     model = Cliente # O un UserCreationForm si se crea un User y un Cliente
#     template_name = 'clientes/registro_form.html'
#     form_class = TuFormularioDeRegistroDeCliente # Necesitaría un form específico
#     success_url = reverse_lazy('login') # O a una página de "registro exitoso"
#     def form_valid(self, form):
#         # Lógica para crear el usuario y/o cliente
#         # user = form.save() # Si es un UserCreationForm
#         # cliente = Cliente.objects.create(user=user, ...)
#         return super().form_valid(form)
