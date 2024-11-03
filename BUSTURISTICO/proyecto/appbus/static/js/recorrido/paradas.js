document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.eliminar-parada').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('¿Estás seguro de que deseas eliminar esta parada del recorrido?')) {
                const paradaId = this.dataset.paradaId;
                fetch(`/recorrido/gestion-paradas/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ eliminar: true, orden_parada_id: paradaId })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        this.closest('.list-group-item').remove();
                    } else {
                        alert('Error al eliminar la parada: ' + data.error);
                    }
                })
                .catch(error => console.error(error));
            }
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie .substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}