document.addEventListener('DOMContentLoaded', function() {
    // Manejar la eliminación de atractivos
    const eliminarBotones = document.querySelectorAll('.eliminar-atractivo');
    
    eliminarBotones.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            
            const asignacionId = this.dataset.asignacionId;
            
            if (confirm('¿Está seguro de que desea eliminar este atractivo de la parada?')) {
                // Crear el formulario para enviar la petición POST
                const form = document.createElement('form');
                form.method = 'POST';
                
                // Agregar el token CSRF
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrfToken;
                
                // Agregar el ID de la asignación y la acción
                const idInput = document.createElement('input');
                idInput.type = 'hidden';
                idInput.name = 'asignacion_id';
                idInput.value = asignacionId;
                
                const actionInput = document.createElement('input');
                actionInput.type = 'hidden';
                actionInput.name = 'eliminar';
                actionInput.value = 'true';
                
                // Agregar todos los inputs al formulario
                form.appendChild(csrfInput);
                form.appendChild(idInput);
                form.appendChild(actionInput);
                
                // Agregar el formulario al documento y enviarlo
                document.body.appendChild(form);
                form.submit();
            }
        });
    });

    // Validación del formulario
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const parada = form.querySelector('[name="parada"]');
            const atractivo = form.querySelector('[name="atractivo"]');
            
            if (!parada.value || !atractivo.value) {
                e.preventDefault();
                alert('Por favor, complete todos los campos requeridos.');
            }
        });
    }
});