# Hotel Premium MVP - Proyecto Django

Bienvenido al proyecto Hotel Premium MVP, una aplicación web desarrollada con Django para la gestión básica de un hotel, incluyendo la visualización de tipos de habitación, servicios y un sistema de reservas.

## Características Clave

*   **Visualización de Información del Hotel:**
    *   Página de inicio atractiva con información configurable desde el admin.
    *   Sección "Sobre Nosotros" detallada.
    *   Galería de imágenes del hotel con modal y paginación.
    *   Página de contacto con formulario funcional y mapa de ubicación.
*   **Gestión de Habitaciones:**
    *   Listado de tipos de habitación con detalles (descripción, capacidad, precio, tipo de cama, tamaño, amenidades).
    *   Galería de imágenes por tipo de habitación con carrusel y miniaturas.
    *   Slugs autogenerados y únicos para URLs amigables.
*   **Gestión de Servicios:**
    *   Listado de servicios del hotel, agrupados por categorías.
    *   Detalle de servicios con información de precio, horario, ubicación.
    *   Categorías de servicios personalizables con iconos.
*   **Sistema de Reservas:**
    *   Formulario público para que los clientes soliciten una reserva.
    *   Validación avanzada de fechas, capacidad y disponibilidad básica.
    *   Página de confirmación de solicitud de reserva con detalles.
    *   Endpoint AJAX para verificación de disponibilidad y precio estimado en tiempo real en el formulario.
    *   Creación/actualización de perfil de cliente al realizar una reserva.
*   **Panel de Administración Django Mejorado:**
    *   Gestión completa de:
        *   Configuración del Sitio (logo, textos, redes sociales, SEO).
        *   Tipos de Habitación (con imágenes inline y amenidades).
        *   Habitaciones Físicas (inventario).
        *   Amenidades de Habitación.
        *   Servicios y Categorías de Servicios.
        *   Clientes (con historial de reservas inline).
        *   Reservas (con huéspedes adicionales inline y acciones personalizadas).
        *   Mensajes de Contacto.
        *   Imágenes de Galería del Hotel.
    *   Uso de `list_display`, `list_filter`, `search_fields`, `readonly_fields`, `fieldsets`, `inlines`, `autocomplete_fields` para una mejor experiencia.
    *   Visualización de iconos FontAwesome en el admin.
*   **SEO Básico:**
    *   Sitemap dinámico (`sitemap.xml`) generado por Django.
    *   Archivo `robots.txt` servido por TemplateView.
    *   Meta tags (descripción, palabras clave) configurables y en plantillas base.
*   **Diseño Responsivo y Moderno:**
    *   Uso de Bootstrap 5.3 para adaptabilidad a diferentes dispositivos.
    *   CSS personalizado para mejorar la estética y UX.
    *   JavaScript para funcionalidades interactivas (scroll-to-top, cierre de alertas, scripts de disponibilidad).
*   **Context Processor Global:**
    *   La configuración del sitio (`ConfiguracionSitio`) está disponible en todas las plantillas a través de la variable `config`.

## Estructura de Directorios

El proyecto sigue la estructura estándar de Django:

```
hotel_premium_mvp/
├── manage.py                 # Utilidad de línea de comandos de Django
├── hotel_project/            # Directorio principal del proyecto Django
│   ├── __init__.py
│   ├── asgi.py               # Configuración ASGI para despliegue
│   ├── settings.py           # Configuración global del proyecto
│   ├── urls.py               # URLs globales del proyecto
│   └── wsgi.py               # Configuración WSGI para despliegue
├── core/                     # App para funcionalidad central
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py # Para la config global
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── sitemaps.py
│   ├── templates/core/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── habitaciones/             # App para gestión de habitaciones
│   ├── ... (estructura similar)
├── reservas/                 # App para gestión de reservas
│   ├── templates/reservas/snippets/ # Para scripts JS
│   ├── ...
├── clientes/                 # App para gestión de clientes
│   ├── ...
├── servicios/                # App para gestión de servicios
│   ├── ...
├── templates/                # Plantillas HTML globales y base
│   ├── base.html
│   ├── footer.html
│   ├── navbar.html
│   └── registration/         # Plantillas para autenticación (ej. login)
├── static/                   # Archivos estáticos (CSS, JS, imágenes globales)
│   ├── css/custom.css
│   ├── js/custom.js
│   ├── img/                  # Placeholders y/o imágenes de diseño base
│   └── robots.txt            # Servido por TemplateView
├── media/                    # Directorio para archivos subidos por usuarios (ej. imágenes)
├── requirements.txt          # Dependencias de Python del proyecto
└── README.md                 # Este archivo
```

## Instrucciones de Configuración y Ejecución (Desde Cero)

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### 1. Requisitos Previos

*   **Python:** Versión 3.8.10 o superior (recomendado 3.9+).
    *   Descarga desde [python.org](https://www.python.org/downloads/).
    *   Asegúrate de que Python y pip estén en el PATH de tu sistema.
*   **Git (Opcional):** Si clonas desde un repositorio. Para este caso, asume que copias los archivos.
*   **Navegador Web:** Chrome, Firefox, Edge, etc.

### 2. Descarga del Código

*   Copia todos los archivos y carpetas proporcionados en una nueva carpeta en tu sistema. Nombra esta carpeta raíz como `hotel_premium_mvp`.

### 3. Crear y Activar el Entorno Virtual

Es altamente recomendable usar un entorno virtual.

*   Abre una terminal o línea de comandos.
*   Navega hasta el directorio raíz del proyecto (`hotel_premium_mvp`):
    ```bash
    cd ruta/a/tu/hotel_premium_mvp
    ```
*   Crea el entorno virtual (ej. `venv`):
    ```bash
    python -m venv venv
    ```
*   Activa el entorno virtual:
    *   **Windows (cmd.exe):** `venv\Scripts\activate.bat`
    *   **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
        (Si hay error de ejecución de scripts, ejecuta: `Set-ExecutionPolicy Unrestricted -Scope Process`)
    *   **Linux/macOS:** `source venv/bin/activate`
    Verás `(venv)` al inicio de tu prompt.

### 4. Instalar Dependencias

Con el entorno virtual activo:
```bash
pip install -r requirements.txt
```

### 5. Aplicar Migraciones de Base de Datos

Esto crea las tablas en la base de datos (SQLite por defecto).
*   Asegúrate de estar en el directorio raíz del proyecto (`hotel_premium_mvp`).
*   Ejecuta:
    ```bash
    python manage.py makemigrations
    ```
    (Este comando prepara archivos de migración si hay cambios en modelos no reflejados. La primera vez, si los archivos de migración ya están incluidos en las apps, este comando puede no generar nuevos archivos para esas apps, pero es buena práctica ejecutarlo).
    ```bash
    python manage.py migrate
    ```
    Esto aplicará las migraciones y creará `db.sqlite3` y las tablas.

### 6. Crear un Superusuario

Para acceder al panel de administración de Django:
```bash
python manage.py createsuperuser
```
Sigue las instrucciones (usuario, email opcional, contraseña).

### 7. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```
El servidor se ejecutará en `http://127.0.0.1:8000/` o `http://localhost:8000/`.

### 8. Acceder al Sitio Web y al Panel de Administración

*   **Sitio Web Público:** `http://127.0.0.1:8000/`
*   **Panel de Administración:** `http://127.0.0.1:8000/admin/` (inicia sesión con el superusuario).

### 9. Configuración Inicial Recomendada (Admin)

1.  **Configuración del Sitio:**
    *   Ve a `Core > 1. Configuraciones del Sitio` y crea una instancia.
    *   Rellena el nombre del hotel, sube un logo, favicon, y completa los campos de contacto, textos de la página de inicio y meta tags SEO.
2.  **Amenidades:**
    *   Ve a `Habitaciones > Amenidades de Habitación` y crea las amenidades que ofrecerás (ej. WiFi, TV, Aire Acondicionado, Minibar, etc.). Puedes usar iconos FontAwesome.
3.  **Tipos de Habitación:**
    *   Ve a `Habitaciones > Tipos de Habitación`. Crea varios tipos (ej. Estándar, Doble, Suite).
    *   Asigna descripciones, capacidad, precio, imagen principal y añade imágenes adicionales en la galería inline.
    *   Selecciona las amenidades correspondientes para cada tipo de habitación.
4.  **Habitaciones Físicas (Inventario):**
    *   Ve a `Habitaciones > Habitaciones Físicas (Inventario)`.
    *   Crea las habitaciones individuales, asignando un número y asociándolas a un `Tipo de Habitación` previamente creado. Define su estado inicial.
5.  **Categorías de Servicios:**
    *   Ve a `Servicios del Hotel > Categorías de Servicios`. Crea categorías como "Restaurante", "Bienestar", "Ocio", etc.
6.  **Servicios:**
    *   Ve a `Servicios del Hotel > Servicios del Hotel`. Crea los servicios específicos, asignándolos a una categoría.
    *   Define precios, horarios, si requieren reserva, etc.
7.  **Galería del Hotel:**
    *   Ve a `Core > Imágenes de Galería del Hotel` y sube imágenes generales del hotel.

### 10. Imágenes de Placeholder

*   El proyecto incluye rutas a imágenes placeholder en `static/img/` (ej. `placeholder_room.jpg`, `hero_default.jpg`). **Debes reemplazar estos archivos con imágenes reales** o asegurar que existan para que el sitio se vea correctamente.
*   El directorio `media/` se creará automáticamente cuando subas la primera imagen a través del admin (ej. logo del hotel, imagen de tipo de habitación).

## Notas Adicionales

*   **SECRET_KEY:** El archivo `settings.py` tiene una `SECRET_KEY` de ejemplo. **NUNCA uses esta clave en un entorno de producción.** Genera una nueva y guárdala de forma segura.
*   **DEBUG:** La variable `DEBUG` en `settings.py` está configurada como `True`. **DEBE ser `False` en producción.**
*   **ALLOWED_HOSTS:** En `settings.py`, `ALLOWED_HOSTS` está vacío. En producción, configúralo con los dominios/IPs de tu aplicación.
*   **Email:** La configuración de email (`EMAIL_BACKEND` en `settings.py`) está para imprimir emails a la consola. Para enviar emails reales, configura un backend SMTP.

## Posibles Futuras Mejoras

*   Integración de pasarela de pago.
*   Autenticación de clientes y panel "Mi Cuenta".
*   Calendario de disponibilidad avanzado.
*   Gestión de tarifas dinámicas y temporadas.
*   Facturación.
*   Internacionalización completa.
*   Tests más exhaustivos.
*   Optimización para producción (Gunicorn/uWSGI, Nginx, base de datos de producción).
*   Sistema de reviews y calificaciones.
*   Blog o sección de noticias.

---

¡Disfruta explorando y trabajando con el proyecto Hotel Premium MVP!
```
