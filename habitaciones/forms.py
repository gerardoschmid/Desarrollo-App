# Contenido de habitaciones/forms.py
from django import forms
from .models import TipoHabitacion # Ejemplo si tuvieras un formulario de búsqueda

# class BusquedaHabitacionForm(forms.Form):
#     fecha_llegada = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
#     fecha_salida = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
#     capacidad = forms.IntegerField(min_value=1, required=False, label="Número de Huéspedes")
#     # Otros campos como rango de precios, amenidades deseadas, etc.

#     def clean(self):
#         cleaned_data = super().clean()
#         llegada = cleaned_data.get("fecha_llegada")
#         salida = cleaned_data.get("fecha_salida")

#         if llegada and salida and salida <= llegada:
#             raise forms.ValidationError("La fecha de salida debe ser posterior a la fecha de llegada.")
#         return cleaned_data

# Por ahora, esta app no requiere formularios públicos complejos más allá de lo que maneja la app 'reservas'.
# Si se necesitara un filtro avanzado en la lista de habitaciones, se podría definir aquí.
