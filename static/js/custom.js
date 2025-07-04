// static/js/custom.js
// Version: 1.1

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar tooltips de Bootstrap (si los usas)
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap (si los usas)
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scroll para anclas (mejorado para evitar errores si el target no existe)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const hrefAttribute = this.getAttribute('href');
            if (hrefAttribute && hrefAttribute.length > 1 && hrefAttribute.startsWith('#')) {
                try {
                    const targetElement = document.querySelector(hrefAttribute);
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth'
                        });
                    }
                } catch (error) {
                    // Si el selector es inválido (ej. href="#!") no hacer nada o loggear error
                    // console.warn('Invalid selector for smooth scroll:', hrefAttribute);
                }
            }
        });
    });

    // Botón Scroll to top
    const scrollTopButton = document.getElementById("scrollTopButton");

    if (scrollTopButton) {
        window.onscroll = function() {
            if (document.body.scrollTop > 150 || document.documentElement.scrollTop > 150) {
                scrollTopButton.classList.remove('d-none');
                // scrollTopButton.classList.add('d-block'); // Bootstrap lo hace visible con d-block
            } else {
                scrollTopButton.classList.add('d-none');
                // scrollTopButton.classList.remove('d-block');
            }
        };

        scrollTopButton.addEventListener('click', function() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }


    // Cerrar alertas de mensajes de Django automáticamente después de un tiempo
    const alerts = document.querySelectorAll('#messages-container .alert-dismissible');
    alerts.forEach(function(alert) {
        // No cerrar automáticamente los errores críticos o advertencias importantes
        if (!alert.classList.contains('alert-danger') && !alert.classList.contains('alert-warning')) {
            setTimeout(function() {
                const bsAlert = bootstrap.Alert.getOrCreateInstance(alert); // Usar getOrCreateInstance
                if (bsAlert) { // Verificar que la instancia se creó/obtuvo
                    bsAlert.close();
                }
            }, 7000); // 7 segundos
        }
    });


    // Lógica para aplicar 'form-control' o 'form-select' a campos de Django si no lo tienen
    // Esto es útil si no usas widgets personalizados en forms.py o django-crispy-forms
    function styleDjangoForms() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input:not([type="checkbox"]):not([type="radio"]):not([type="submit"]):not([type="reset"]):not([type="button"]):not([type="file"]):not([type="hidden"]), select, textarea');
            inputs.forEach(input => {
                if (input.tagName.toLowerCase() === 'select') {
                    if (!input.classList.contains('form-select')) {
                        input.classList.add('form-select');
                    }
                } else {
                    if (!input.classList.contains('form-control')) {
                        input.classList.add('form-control');
                    }
                }
            });
        });
    }
    // Ejecutar al cargar, y podrías re-ejecutarlo si cargas formularios dinámicamente.
    // styleDjangoForms();
    // Nota: En las plantillas de formulario ya se está añadiendo la clase 'form-control' a los widgets
    // o usando Bootstrap directamente, por lo que esta función global puede no ser estrictamente necesaria
    // si los formularios individuales se manejan bien. La dejo como referencia.


    // Añadir 'is-invalid' a los campos de formulario con errores (si Django no lo hace con el widget)
    // Esto es más robusto si se hace del lado del servidor con un custom widget o form renderer.
    // document.querySelectorAll('form .errorlist').forEach(errorList => {
    //     const fieldContainer = errorList.closest('.mb-3, .form-floating'); // Asume una estructura común
    //     if (fieldContainer) {
    //         const inputField = fieldContainer.querySelector('.form-control, .form-select');
    //         if (inputField) {
    //             inputField.classList.add('is-invalid');
    //         }
    //     }
    // });


    // console.log("Custom JS v1.1 cargado y ejecutado.");
});
```
