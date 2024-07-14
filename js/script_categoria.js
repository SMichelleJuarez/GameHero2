document.addEventListener('DOMContentLoaded', () => {
    const juegosContainer = document.getElementById('juegos-container');
    const categoriaNombre = document.getElementById('categoria-title');
    
    const urlParams = new URLSearchParams(window.location.search);
    const idCategoria = urlParams.get('id');
    const categoria = urlParams.get('categoria');

    // URL base del servidor
    const serverURL = "https://SofiaMJuarez.pythonanywhere.com";

    // Actualiza el título de la categoría
    categoriaNombre.textContent = categoria ? categoria : 'Todas las Categorías';

    // Fetch para obtener la categoría por ID si está presente
    if (idCategoria) {
        fetch(`${serverURL}/api/categorias/${idCategoria}`)
            .then(response => response.json())
            .then(categoria => {
                categoriaNombre.innerText = categoria.nombre;
            })
            .catch(error => console.error('Error al cargar la categoría:', error));
    }

    // Fetch para obtener los juegos según la categoría
    fetch(`${serverURL}/api/juegos${idCategoria ? '?categoria=' + idCategoria : ''}`)
        .then(response => response.json())
        .then(juegos => {
            juegosContainer.innerHTML = ''; 
            juegos.forEach(juego => {
                const div = document.createElement('div');
                div.className = 'juego';
                div.innerHTML = `
                    <h2>${juego.titulo}</h2>
                    <img src="${serverURL}/imagenes/${juego.contenido_url}" alt="${juego.titulo}">
                    <p>${juego.resumen}</p>
                    <div class="comentarios" id="comentarios-${juego.id_juego}"></div>
                    <div class="input-comentario">
                        <input type="text" id="comentario-input-${juego.id_juego}" placeholder="Escribe un comentario">
                        <button onclick="agregarComentario(${juego.id_juego})">Comentar</button>
                    </div>
                `;
                juegosContainer.appendChild(div);
                listarComentarios(juego.id_juego);
            });
        })
        .catch(error => console.error('Error al cargar los juegos:', error));
});

function listarComentarios(idJuego) {
    const serverURL = "https://SofiaMJuarez.pythonanywhere.com";

    fetch(`${serverURL}/api/comentarios/${idJuego}`)
        .then(response => response.json())
        .then(comentarios => {
            const comentariosContainer = document.getElementById(`comentarios-${idJuego}`);
            comentariosContainer.innerHTML = '';
            comentarios.forEach(comentario => {
                const div = document.createElement('div');
                div.className = 'comentario';
                div.innerHTML = `
                    <p>${comentario.texto}</p>
                    <button onclick="eliminarComentario(${comentario.id_comentario}, ${idJuego})">Eliminar</button>
                `;
                comentariosContainer.appendChild(div);
            });
        });
}

function agregarComentario(idJuego) {
    const serverURL = "https://SofiaMJuarez.pythonanywhere.com";
    const input = document.getElementById(`comentario-input-${idJuego}`);
    const texto = input.value;

    if (texto.trim() === '') {
        alert('El comentario no puede estar vacío');
        return;
    }

    fetch(`${serverURL}/api/comentarios`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            texto,
            id_juego: idJuego
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.id_comentario) {
            listarComentarios(idJuego);
            input.value = '';
        } else {
            alert('Error al agregar el comentario');
        }
    });
}

function eliminarComentario(idComentario, idJuego) {
    const serverURL = "https://SofiaMJuarez.pythonanywhere.com";

    fetch(`${serverURL}/api/comentarios/${idComentario}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            listarComentarios(idJuego);
        } else {
            alert('Error al eliminar el comentario');
        }
    });
}
