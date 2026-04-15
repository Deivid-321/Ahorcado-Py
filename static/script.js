let juegoActivo = true;

// Cargar el estado inicial del juego
window.addEventListener('load', () => {
    actualizarEstado();
});

// Permitir Enter para adivinar
document.getElementById('letterInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && juegoActivo) {
        adivinarLetra();
    }
});

async function actualizarEstado() {
    try {
        const response = await fetch('/api/estado');
        const data = await response.json();

        // Actualizar dibujo del ahorcado
        document.getElementById('hangmanDrawing').textContent = data.ahorcado;

        // Actualizar palabra mostrada
        const palabraMostrada = data.palabra_mostrada
            .split('')
            .join(' ');
        document.getElementById('wordDisplay').textContent = palabraMostrada;
        document.getElementById('wordLength').textContent = data.palabra_mostrada.length;
        document.getElementById('hintText').textContent = data.pista || 'Pista disponible en la siguiente ronda.';

        // Actualizar intentos
        document.getElementById('attempts').textContent = data.intentos;

        // Actualizar letras incorrectas
        const incorrectasText = data.letras_incorrectas.length > 0
            ? data.letras_incorrectas.join(', ')
            : '-';
        document.getElementById('incorrectLetters').textContent = incorrectasText;

        // Limpiar mensaje
        document.getElementById('message').textContent = '';
        document.getElementById('message').className = 'message';

        // Verificar si el juego terminó
        if (data.gano) {
            juegoActivo = false;
            document.getElementById('message').textContent = '¡🎉 ¡GANASTE! 🎉';
            document.getElementById('message').className = 'message win';
            document.getElementById('guessButton').disabled = true;
            document.getElementById('letterInput').disabled = true;
        } else if (data.perdio) {
            juegoActivo = false;
            document.getElementById('message').textContent = `😢 Perdiste... La palabra era: ${data.palabra_secreta}`;
            document.getElementById('message').className = 'message lose';
            document.getElementById('guessButton').disabled = true;
            document.getElementById('letterInput').disabled = true;
        }

    } catch (error) {
        console.error('Error:', error);
    }
}

async function adivinarLetra() {
    if (!juegoActivo) return;

    const input = document.getElementById('letterInput');
    const letra = input.value.trim().toUpperCase();

    if (!letra) {
        mostrarMensaje('Por favor, ingresa una letra', 'error');
        return;
    }

    if (!/^[A-Z]$/.test(letra)) {
        mostrarMensaje('Solo se permiten letras', 'error');
        input.value = '';
        return;
    }

    try {
        const response = await fetch(`/api/adivinar/${letra}`, {
            method: 'POST'
        });

        if (response.status === 400) {
            const data = await response.json();
            mostrarMensaje(data.error, 'error');
        } else {
            actualizarEstado();
        }

        input.value = '';
        input.focus();

    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje('Error al procesar la adivinanza', 'error');
    }
}

async function nuevoJuego() {
    try {
        const response = await fetch('/api/nuevo_juego', {
            method: 'POST'
        });

        if (response.ok) {
            juegoActivo = true;
            document.getElementById('letterInput').disabled = false;
            document.getElementById('guessButton').disabled = false;
            document.getElementById('letterInput').value = '';
            document.getElementById('letterInput').focus();
            actualizarEstado();
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function mostrarMensaje(texto, tipo) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = texto;
    messageEl.className = `message ${tipo}`;
}
