# 🎮 Ahorcadito con IA

Un juego del ahorcado moderno que genera palabras dinámicas usando Inteligencia Artificial.

## ✨ Características

- 🎯 **Palabras dinámicas**: Cada juego genera una palabra diferente usando IA
- 🌐 **Web moderna**: Interfaz responsive con diseño atractivo
- 🤖 **IA integrada**: Soporte para HuggingFace y OpenAI
- ⚡ **Rápido**: API gratuita de palabras aleatorias como opción principal
- 🔄 **Respaldo**: Lista de palabras predefinidas si falla la IA

## 🚀 Instalación

1. **Clona o descarga** los archivos del proyecto
2. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura tu API** en el archivo `.env`:
   ```bash
   # Para HuggingFace (Recomendado - ¡Gratuito!)
   AI_SERVICE=huggingface
   HUGGINGFACE_API_KEY=tu_token_aqui

   # Para OpenAI (Pago)
   AI_SERVICE=openai
   OPENAI_API_KEY=tu_token_aqui
   ```

4. **Ejecuta el servidor**:
   ```bash
   python app.py
   ```

5. **¡Juega!** Abre http://127.0.0.1:5000 en tu navegador

## 🎮 Cómo Jugar

1. **Adivina letras**: Ingresa una letra por vez
2. **6 intentos**: Tienes 6 oportunidades antes de perder
3. **Palabras variadas**: Cada partida tiene una palabra diferente generada por IA
4. **Nuevo juego**: Haz clic en "Nuevo Juego" para empezar otra partida

## 🤖 Sistema de IA

### Opción 1: API Gratuita (Recomendada)
- **Servicio**: Random Word API
- **Ventajas**: Rápida, confiable, ¡gratis!
- **Idiomas**: Español
- **Límite**: 4-10 letras

### Opción 2: HuggingFace
- **Servicio**: Modelos de lenguaje de HuggingFace
- **Ventajas**: IA avanzada, personalizable
- **Costo**: Gratuito (con límites)
- **Registro**: https://huggingface.co/join

### Opción 3: OpenAI
- **Servicio**: GPT-3.5 Turbo
- **Ventajas**: IA de alta calidad
- **Costo**: Pago por uso
- **Registro**: https://platform.openai.com

```

## 🔧 Configuración Avanzada

### Variables de Entorno (.env)
```bash
# Activar/desactivar IA
USE_AI=true

# Servicio a usar
AI_SERVICE=huggingface  # 'huggingface' o 'openai'

# Tokens de API
HUGGINGFACE_API_KEY=tu_clave_api_aqui
OPENAI_API_KEY=tu_clave_openai_aqui
```

### Personalización
- **Palabras de respaldo**: Edita `PALABRAS_RESPALDO` en `app.py`
- **Dificultad**: Modifica `len(HANGMAN_STATES) - 1` para cambiar intentos
- **Estilos**: Personaliza `static/style.css`

## 🧪 Pruebas

Para probar la generación de palabras:
```bash
python test_ia.py
```

Esto generará 10 palabras de ejemplo y mostrará estadísticas.

## 📝 API Endpoints

- `GET /`: Página principal
- `GET /api/estado`: Estado actual del juego
- `POST /api/adivinar/<letra>`: Adivinar una letra
- `POST /api/nuevo_juego`: Iniciar nuevo juego

## 🎨 Tecnologías

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: HuggingFace API / OpenAI API
- **Estilos**: CSS moderno con gradientes y animaciones

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Ideas para mejorar:
- Más temas de palabras (animales, países, comida, etc.)
- Modos de dificultad
- Estadísticas de jugador
- Modo multijugador
- Soporte para más idiomas

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de usarlo y modificarlo.

---

¡Diviértete jugando y programando! 🎉</content>
<parameter name="filePath">c:\Users\deivi\OneDrive\Desktop\Ahorcadito\README.md