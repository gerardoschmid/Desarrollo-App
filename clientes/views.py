# Contenido de clientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .models import Cliente
# from .forms import ClienteProfileForm # Si tuvieras un formulario para que el cliente edite su perfil

# @login_required
# def perfil_cliente_view(request):
#     """
#     Vista para que un cliente autenticado vea y edite su perfil.
#     Asume que tienes una relación OneToOneField o ForeignKey desde tu modelo User
#     al modelo Cliente, o una forma de obtener el Cliente asociado al request.user.
#     """
#     try:
#         # Intenta obtener el perfil del cliente. Esto depende de cómo hayas relacionado Cliente con User.
#         # Opción 1: Si Cliente tiene un campo 'user' ForeignKey o OneToOneField a User
#         cliente = get_object_or_404(Cliente, user=request.user)
#         # Opción 2: Si User tiene un campo OneToOneField a Cliente (ej. 'cliente_profile')
#         # cliente = request.user.cliente_profile
#     except Cliente.DoesNotExist:
#         # Manejar el caso donde un usuario autenticado no tiene un perfil de Cliente asociado.
#         # Podrías crearlo aquí, o redirigir, o mostrar un mensaje.
#         messages.error(request, "No se encontró un perfil de cliente asociado a tu cuenta.")
#         return redirect('core:index') # O a una página de error/información

#     if request.method == 'POST':
#         form = ClienteProfileForm(request.POST, request.FILES, instance=cliente) # request.FILES si hay subida de archivos
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Tu perfil ha sido actualizado correctamente.")
#             return redirect('clientes:perfil_cliente') # Redirigir a la misma vista
#         else:
#             messages.error(request, "Por favor corrige los errores en el formulario.")
#     else:
#         form = ClienteProfileForm(instance=cliente)

#     context = {
#         'form': form,
#         'cliente': cliente,
#         # 'page_title': "Mi Perfil", # El título se puede manejar en la plantilla base
#     }
#     return render(request, 'clientes/perfil_cliente.html', context)


# @login_required
# def mis_reservas_view(request):
#     """
#     Vista para que un cliente autenticado vea su historial de reservas.
#     """
#     try:
#         cliente = get_object_or_404(Cliente, user=request.user)
#         # Obtener las reservas del cliente, ordenadas por fecha de llegada (más recientes primero)
#         # Asegúrate que el related_name en la FK de Reserva a Cliente sea 'reservas_cliente'
#         reservas_del_cliente = cliente.reservas_cliente.all().order_by('-fecha_llegada', '-fecha_creacion')
#     except Cliente.DoesNotExist:
#         messages.error(request, "No se encontró un perfil de cliente asociado a tu cuenta.")
#         return redirect('core:index')

#     context = {
#         'reservas_del_cliente': reservas_del_cliente,
#         # 'page_title': "Mis Reservas",
#     }
#     return render(request, 'clientes/mis_reservas.html', context)

# Por ahora, la app 'clientes' se enfoca en el backend (admin).
# Si en el futuro se añaden vistas para el frontend (ej. perfil de cliente),
# se implementarán aquí.
```
