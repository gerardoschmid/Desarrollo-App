from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Servicio
# from .forms import ServicioForm # Si se necesita un formulario personalizado
from django.contrib.auth.mixins import LoginRequiredMixin # Para vistas de gestión

# Vistas Públicas
class ListaServiciosView(ListView):
    model = Servicio
    template_name = 'servicios/lista_servicios.html' # Template para el público
    context_object_name = 'servicios'
    queryset = Servicio.objects.filter(disponible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Nuestros Servicios"
        return context

class DetalleServicioView(DetailView):
    model = Servicio
    template_name = 'servicios/detalle_servicio.html' # Template para el público
    context_object_name = 'servicio'
    queryset = Servicio.objects.filter(disponible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.nombre if self.object else "Detalle del Servicio"
        return context

# Vistas de Gestión (CRUD - podrían requerir LoginRequiredMixin o PermissionRequiredMixin)
# class ServicioListView(LoginRequiredMixin, ListView): # Ejemplo con LoginRequiredMixin
class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicios/admin_lista_servicios.html' # Template para gestión
    context_object_name = 'servicios'
    # paginate_by = 10 # Opcional: paginación

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestión de Servicios"
        return context

# class ServicioDetailView(LoginRequiredMixin, DetailView): # Vista de detalle para admin
class ServicioDetailView(DetailView):
    model = Servicio
    template_name = 'servicios/admin_detalle_servicio.html'
    context_object_name = 'servicio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Detalle: {self.object.nombre}" if self.object else "Detalle del Servicio"
        return context

# class ServicioCreateView(LoginRequiredMixin, CreateView):
class ServicioCreateView(CreateView):
    model = Servicio
    template_name = 'servicios/servicio_form.html' # Usar un solo form para crear/editar
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'disponible'] # O usar form_class
    # form_class = ServicioForm
    success_url = reverse_lazy('servicios:admin_lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Crear Nuevo Servicio"
        context['form_title'] = "Registrar Servicio"
        context['submit_button_text'] = "Guardar Servicio"
        return context

    # def form_valid(self, form):
    #     # Lógica adicional si es necesaria antes de guardar
    #     return super().form_valid(form)

# class ServicioUpdateView(LoginRequiredMixin, UpdateView):
class ServicioUpdateView(UpdateView):
    model = Servicio
    template_name = 'servicios/servicio_form.html'
    fields = ['nombre', 'descripcion', 'precio', 'imagen', 'disponible']
    # form_class = ServicioForm
    success_url = reverse_lazy('servicios:admin_lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editar: {self.object.nombre}" if self.object else "Editar Servicio"
        context['form_title'] = f"Editando Servicio: {self.object.nombre}" if self.object else "Editar Servicio"
        context['submit_button_text'] = "Actualizar Servicio"
        return context

# class ServicioDeleteView(LoginRequiredMixin, DeleteView):
class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'servicios/servicio_confirm_delete.html'
    success_url = reverse_lazy('servicios:admin_lista_servicios')
    context_object_name = 'servicio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Confirmar Eliminación: {self.object.nombre}" if self.object else "Eliminar Servicio"
        return context
