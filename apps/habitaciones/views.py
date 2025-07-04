from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Habitacion, TipoHabitacion, ImagenHabitacion
# from .forms import HabitacionForm, TipoHabitacionForm # Si se necesitan formularios personalizados
from django.contrib.auth.mixins import LoginRequiredMixin

# Vistas Públicas para Tipos de Habitación
class ListaTiposHabitacionView(ListView):
    model = TipoHabitacion
    template_name = 'habitaciones/lista_tipos_habitacion.html' # Galería pública de tipos
    context_object_name = 'tipos_habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Nuestros Tipos de Habitación"
        # Para cada tipo de habitación, podríamos querer mostrar una imagen representativa
        # Esto se puede manejar en el modelo TipoHabitacion con un método o aquí en la vista.
        for tipo in context['tipos_habitacion']:
            primera_habitacion_del_tipo = Habitacion.objects.filter(tipo_habitacion=tipo).first()
            if primera_habitacion_del_tipo:
                tipo.imagen_representativa = ImagenHabitacion.objects.filter(habitacion=primera_habitacion_del_tipo).first()
            else:
                tipo.imagen_representativa = None
        return context

class DetalleTipoHabitacionView(DetailView):
    model = TipoHabitacion
    template_name = 'habitaciones/detalle_tipo_habitacion.html' # Detalle público de un tipo
    context_object_name = 'tipo_habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tipo = self.object
        context['page_title'] = tipo.nombre if tipo else "Detalle del Tipo de Habitación"

        habitaciones_del_tipo = Habitacion.objects.filter(tipo_habitacion=tipo, disponible=True).prefetch_related('imagenes')
        context['habitaciones_del_tipo'] = habitaciones_del_tipo

        # Recopilar imágenes para la galería del tipo de habitación
        imagenes_tipo_galeria = []
        # Intentar obtener una imagen principal más destacada (ej. la primera imagen de la primera habitación)
        context['imagen_principal_tipo'] = None

        for habitacion in habitaciones_del_tipo:
            for img in habitacion.imagenes.all():
                if not context['imagen_principal_tipo']: # Tomar la primera imagen encontrada como principal
                    context['imagen_principal_tipo'] = img
                imagenes_tipo_galeria.append(img)

        # Si no se encontró una imagen principal pero hay imágenes en la galería, tomar la primera de ahí
        if not context['imagen_principal_tipo'] and imagenes_tipo_galeria:
            context['imagen_principal_tipo'] = imagenes_tipo_galeria[0]

        context['imagenes_tipo_galeria'] = list(set(imagenes_tipo_galeria)) # Eliminar duplicados si alguna imagen se comparte o procesa dos veces

        # Características (tomadas de la primera habitación como referencia, idealmente TipoHabitacion tendría campos propios)
        primera_habitacion = habitaciones_del_tipo.first()
        if primera_habitacion:
            context['capacidad_tipo'] = primera_habitacion.capacidad
            context['precio_desde_tipo'] = primera_habitacion.precio_por_noche
            # Aquí se podrían añadir más campos si TipoHabitacion tuviera comodidades, etc.
            # Ejemplo: context['comodidades_tipo'] = tipo.comodidades.all() (si existiera un ManyToManyField)

        return context

# Vistas de Gestión para Habitaciones (CRUD)
# class HabitacionListView(LoginRequiredMixin, ListView):
class HabitacionListView(ListView):
    model = Habitacion
    template_name = 'habitaciones/admin_lista_habitaciones.html'
    context_object_name = 'habitaciones'
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Gestión de Habitaciones"
        return context

# class HabitacionDetailView(LoginRequiredMixin, DetailView):
class HabitacionDetailView(DetailView):
    model = Habitacion
    template_name = 'habitaciones/admin_detalle_habitacion.html' # Detalle para admin
    context_object_name = 'habitacion'
    slug_field = 'numero_habitacion' # Si usamos el número de habitación en la URL
    slug_url_kwarg = 'numero_habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Habitación {self.object.numero_habitacion}" if self.object else "Detalle de Habitación"
        return context

# class HabitacionCreateView(LoginRequiredMixin, CreateView):
class HabitacionCreateView(CreateView):
    model = Habitacion
    template_name = 'habitaciones/habitacion_form.html'
    fields = ['numero_habitacion', 'tipo_habitacion', 'capacidad', 'precio_por_noche', 'disponible', 'descripcion_adicional']
    # form_class = HabitacionForm
    success_url = reverse_lazy('habitaciones:admin_lista_habitaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Registrar Nueva Habitación"
        context['form_title'] = "Datos de la Nueva Habitación"
        context['submit_button_text'] = "Guardar Habitación"
        return context

# class HabitacionUpdateView(LoginRequiredMixin, UpdateView):
class HabitacionUpdateView(UpdateView):
    model = Habitacion
    template_name = 'habitaciones/habitacion_form.html'
    fields = ['tipo_habitacion', 'capacidad', 'precio_por_noche', 'disponible', 'descripcion_adicional']
    # form_class = HabitacionForm
    slug_field = 'numero_habitacion'
    slug_url_kwarg = 'numero_habitacion'
    success_url = reverse_lazy('habitaciones:admin_lista_habitaciones')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Editar Habitación {self.object.numero_habitacion}" if self.object else "Editar Habitación"
        context['form_title'] = f"Editando Habitación: {self.object.numero_habitacion}" if self.object else "Editar Habitación"
        context['submit_button_text'] = "Actualizar Habitación"
        return context

# class HabitacionDeleteView(LoginRequiredMixin, DeleteView):
class HabitacionDeleteView(DeleteView):
    model = Habitacion
    template_name = 'habitaciones/habitacion_confirm_delete.html'
    slug_field = 'numero_habitacion'
    slug_url_kwarg = 'numero_habitacion'
    success_url = reverse_lazy('habitaciones:admin_lista_habitaciones')
    context_object_name = 'habitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Eliminar Habitación {self.object.numero_habitacion}" if self.object else "Eliminar Habitación"
        return context

# Faltarían vistas para ImagenHabitacion y TipoHabitacion CRUD si se gestionan fuera del admin de Django.
# Por simplicidad, se asume que se gestionarán principalmente desde el admin o inline con la habitación.
# Ejemplo para TipoHabitacion (si se necesita un CRUD completo fuera del admin)
# class TipoHabitacionListView(LoginRequiredMixin, ListView): ...
# class TipoHabitacionCreateView(LoginRequiredMixin, CreateView): ...
# class TipoHabitacionUpdateView(LoginRequiredMixin, UpdateView): ...
# class TipoHabitacionDeleteView(LoginRequiredMixin, DeleteView): ...
