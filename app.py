from flask import Flask, render_template, request, jsonify, session
import random
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'ahorcadito_secret_key_2026'

# Configuración para IA
USE_AI = True
AI_SERVICE = os.getenv('AI_SERVICE', 'huggingface')  # 'huggingface' o 'openai'
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Lista de palabras como respaldo si falla la IA
PALABRAS_RESPALDO = [
    'python', 'flask', 'programacion', 'computadora', 'desarrollo',
    'inteligencia', 'algoritmo', 'variable', 'función', 'módulo',
    'javascript', 'database', 'servidor', 'cliente', 'navegador',
    'internet', 'tecnologia', 'software', 'hardware', 'codigo',
    'gato', 'perro', 'pajaro', 'serpiente', 'elefante',
    'montaña', 'rio', 'bosque', 'playa', 'desierto',
    'libro', 'película', 'musica', 'deporte', 'juego'
]

# Estados del ahorcado (ASCII art)
HANGMAN_STATES = [
    # Estado 0: vacío
    """
       +---+
       |   |
           |
           |
           |
           |
    """,
    # Estado 1: cabeza
    """
       +---+
       |   |
       O   |
           |
           |
           |
    """,
    # Estado 2: cuerpo
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    """,
    # Estado 3: brazo izquierdo
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    """,
    # Estado 4: brazo derecho
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    """,
    # Estado 5: pierna izquierda
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    """,
    # Estado 6: pierna derecha (game over)
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    """
]


def generar_palabra_api_gratuita():
    """Genera una palabra usando una API gratuita de palabras aleatorias"""
    try:
        # Usar la API de palabras aleatorias (gratuita y confiable)
        response = requests.get('https://random-word-api.herokuapp.com/word?lang=es', timeout=5)
        response.raise_for_status()

        palabras = response.json()
        if isinstance(palabras, list) and len(palabras) > 0:
            palabra = palabras[0].lower()
            palabra = ''.join(c for c in palabra if c.isalpha())
            if 4 <= len(palabra) <= 10:
                return palabra

    except Exception as e:
        print(f"API gratuita falló: {e}")

    return random.choice(PALABRAS_RESPALDO)


def generar_palabra_con_ia():
    """Genera una palabra aleatoria usando IA"""
    if not USE_AI:
        return random.choice(PALABRAS_RESPALDO)

    try:
        # Primero intentar con API gratuita (más rápida y confiable)
        return generar_palabra_api_gratuita()
    except:
        pass

    try:
        # Si falla, usar HuggingFace como respaldo
        if AI_SERVICE == 'openai' and OPENAI_API_KEY:
            return generar_palabra_openai()
        elif AI_SERVICE == 'huggingface' and HUGGINGFACE_API_KEY:
            return generar_palabra_huggingface()
        else:
            return random.choice(PALABRAS_RESPALDO)
    except Exception as e:
        print(f"Error al generar palabra con IA: {e}")
        return random.choice(PALABRAS_RESPALDO)


def generar_palabra_openai():
    """Genera una palabra usando OpenAI API"""
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [
            {
                'role': 'user',
                'content': 'Genera UNA sola palabra en español, común, sin tilde, entre 4 y 10 letras. Solo responde con la palabra, nada más.'
            }
        ],
        'max_tokens': 20,
        'temperature': 0.7
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions', 
                            headers=headers, json=data, timeout=5)
    response.raise_for_status()
    
    palabra = response.json()['choices'][0]['message']['content'].strip().lower()
    # Limpiar la palabra de caracteres especiales
    palabra = ''.join(c for c in palabra if c.isalpha())
    return palabra if len(palabra) >= 4 else random.choice(PALABRAS_RESPALDO)


def generar_palabra_huggingface():
    """Genera una palabra usando HuggingFace Inference API"""
    headers = {'Authorization': f'Bearer {HUGGINGFACE_API_KEY}'}

    prompt = 'Genera UNA sola palabra en español, común, sin tilde, entre 4 y 10 letras. '

    data = {
        'inputs': prompt,
        'parameters': {
            'max_new_tokens': 15,
            'temperature': 0.8,
            'do_sample': True,
            'top_p': 0.9
        }
    }

    # Intentar con diferentes modelos en orden de preferencia
    modelos = [
        'microsoft/DialoGPT-medium',
        'distilgpt2',
        'gpt2'
    ]

    for modelo in modelos:
        try:
            response = requests.post(
                f'https://api-inference.huggingface.co/models/{modelo}',
                headers=headers, json=data, timeout=8
            )
            response.raise_for_status()

            resultado = response.json()
            if isinstance(resultado, list) and len(resultado) > 0:
                texto = resultado[0].get('generated_text', '')
                # Limpiar y extraer la palabra
                texto_limpio = texto.replace(prompt, '').strip()
                palabras = texto_limpio.split()
                palabra = palabras[0].lower() if palabras else ''
                palabra = ''.join(c for c in palabra if c.isalpha())

                if 4 <= len(palabra) <= 10:
                    return palabra

        except Exception as e:
            print(f"Modelo {modelo} falló: {e}")
            continue

    # Si todos los modelos fallan, usar respaldo
    return random.choice(PALABRAS_RESPALDO)

def generar_pista_ia(palabra):
    """Genera una pista tipo acertijo con IA para cualquier palabra."""
    if not USE_AI:
        return None

    prompt = (
        f"Escribe una pista tipo acertijo en español para la palabra '{palabra}'. "
        "No menciones la palabra ni ninguna letra exacta. Usa solo una frase."
    )

    if AI_SERVICE == 'openai' and OPENAI_API_KEY:
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 40,
                'temperature': 0.7
            }
            response = requests.post('https://api.openai.com/v1/chat/completions',
                                     headers=headers, json=data, timeout=8)
            response.raise_for_status()
            texto = response.json()['choices'][0]['message']['content'].strip()
            return texto
        except Exception as e:
            print(f"Error al generar pista con OpenAI: {e}")
            return None

    if AI_SERVICE == 'huggingface' and HUGGINGFACE_API_KEY:
        try:
            headers = {'Authorization': f'Bearer {HUGGINGFACE_API_KEY}'}
            data = {
                'inputs': prompt,
                'parameters': {
                    'max_new_tokens': 40,
                    'temperature': 0.7,
                    'do_sample': True,
                    'top_p': 0.9
                }
            }
            response = requests.post(
                'https://api-inference.huggingface.co/models/distilgpt2',
                headers=headers, json=data, timeout=10
            )
            response.raise_for_status()
            resultado = response.json()
            if isinstance(resultado, list) and len(resultado) > 0:
                texto = resultado[0].get('generated_text', '').strip()
                texto = texto.replace(prompt, '').strip()
                return texto
        except Exception as e:
            print(f"Error al generar pista con HuggingFace: {e}")
            return None

    return None

def crear_pista(palabra):
    """Crea una pista con una letra no adivinada de la palabra y un acertijo."""
    pistas_especiales = {
        'python': 'Es un lenguaje famoso entre programadores.',
        'flask': 'Es un marco de trabajo para aplicaciones web en Python.',
        'programacion': 'Es el proceso de crear instrucciones para una computadora.',
        'computadora': 'Es una máquina que procesa datos y ejecuta programas.',
        'desarrollo': 'Es lo que haces al construir software o una aplicación.',
        'inteligencia': 'Es la capacidad de pensar, aprender y resolver problemas.',
        'algoritmo': 'Es una serie de pasos para resolver un problema.',
        'variable': 'En programación, es un nombre que almacena un valor.',
        'función': 'Es un bloque de código que realiza una tarea específica.',
        'módulo': 'Es una parte separada de un programa o librería.',
        'javascript': 'Es un lenguaje que hace que las páginas web sean interactivas.',
        'database': 'Es un lugar donde se guarda información organizada.',
        'servidor': 'Es una máquina que entrega datos a otras máquinas o usuarios.',
        'cliente': 'Es el que recibe servicios de un servidor.',
        'navegador': 'Es el programa que usas para ver páginas web.',
        'internet': 'Es la red global que conecta computadoras en todo el mundo.',
        'tecnologia': 'Es todo lo relacionado con dispositivos y herramientas modernas.',
        'software': 'Es el conjunto de programas que usa una computadora.',
        'hardware': 'Son las partes físicas de una computadora.',
        'codigo': 'Son instrucciones que escribe el programador.',
        'gato': 'Es un animal doméstico que dice "miau".',
        'perro': 'Es un animal fiel que suele decir "guau".',
        'pajaro': 'Es un animal que puede volar y tiene plumas.',
        'serpiente': 'Es un animal alargado que se arrastra sin patas.',
        'elefante': 'Es un animal grande con trompa y colmillos.',
        'montaña': 'Es una elevación de terreno muy alta.',
        'rio': 'Es un curso de agua que fluye hacia el mar.',
        'bosque': 'Es un lugar con muchos árboles.',
        'playa': 'Es donde la tierra se encuentra con el mar.',
        'desierto': 'Es un lugar seco con muy poca agua.',
        'libro': 'Es un conjunto de hojas con texto o historias.',
        'película': 'Es una historia que ves en la pantalla.',
        'musica': 'Son sonidos organizados que escuchas con gusto.',
        'deporte': 'Es una actividad física con reglas y competencia.',
        'juego': 'Es una actividad para divertirse y competir.'
    }

    letras_unicas = [letra for letra in set(palabra) if letra.isalpha()]
    pista_letra = random.choice(letras_unicas) if letras_unicas else None
    pista_letra_texto = f'La palabra contiene la letra "{pista_letra}".' if pista_letra else ''

    clave = palabra.lower()
    pista_texto = pistas_especiales.get(clave)
    if not pista_texto:
        pista_texto = generar_pista_ia(clave)
    if not pista_texto:
        # Mejor fallback para palabras IA sin pista especial
        if clave.endswith('o'):
            categoria = 'un término masculino o un objeto común'
        elif clave.endswith('a'):
            categoria = 'algo que podría ser femenino o un sustantivo suave'
        elif clave.endswith('e'):
            categoria = 'una palabra moderna o neutra'
        else:
            categoria = 'una palabra interesante que debes descubrir'

        vocales = ''.join(sorted(set([c for c in clave if c in 'aeiou'])))
        if vocales:
            pista_texto = (
                f'Es una palabra de {len(clave)} letras que usa las vocales {vocales}. '
                f'Piensa en {categoria}.'
            )
        else:
            pista_texto = f'Es una palabra de {len(clave)} letras que debes adivinar como en un acertijo.'

    return f'{pista_letra_texto} {pista_texto}'

def iniciar_nuevo_juego():
    """Inicia un nuevo juego"""
    palabra_secreta = generar_palabra_con_ia().upper()
    session['palabra_secreta'] = palabra_secreta
    session['pista'] = crear_pista(palabra_secreta)
    session['letras_adivinadas'] = []
    session['letras_incorrectas'] = []
    session['intentos'] = 0
    session['juego_terminado'] = False
    session['gano'] = False


@app.route('/')
def index():
    """Página principal"""
    if 'palabra_secreta' not in session:
        iniciar_nuevo_juego()
    return render_template('index.html')


@app.route('/api/estado')
def obtener_estado():
    """Obtiene el estado actual del juego"""
    if 'palabra_secreta' not in session:
        iniciar_nuevo_juego()
    
    palabra_secreta = session.get('palabra_secreta', '')
    letras_adivinadas = session.get('letras_adivinadas', [])
    letras_incorrectas = session.get('letras_incorrectas', [])
    intentos = session.get('intentos', 0)
    
    # Construir la palabra mostrada
    palabra_mostrada = ''.join(
        [letra if letra in letras_adivinadas else '_' 
         for letra in palabra_secreta]
    )
    
    # Verificar si ganó
    gano = '_' not in palabra_mostrada and palabra_mostrada != ''
    
    # Verificar si perdió
    perdio = intentos >= len(HANGMAN_STATES) - 1
    
    return jsonify({
        'palabra_mostrada': palabra_mostrada,
        'letras_incorrectas': letras_incorrectas,
        'letras_adivinadas': letras_adivinadas,
        'intentos': intentos,
        'max_intentos': len(HANGMAN_STATES) - 1,
        'ahorcado': HANGMAN_STATES[min(intentos, len(HANGMAN_STATES) - 1)],
        'pista': session.get('pista', ''),
        'gano': gano,
        'perdio': perdio,
        'palabra_secreta': palabra_secreta if (gano or perdio) else None
    })


@app.route('/api/adivinar/<letra>', methods=['POST'])
def adivinar_letra(letra):
    """Procesa la adivinanza de una letra"""
    if 'palabra_secreta' not in session:
        iniciar_nuevo_juego()
    
    letra = letra.upper()
    palabra_secreta = session.get('palabra_secreta', '')
    letras_adivinadas = session.get('letras_adivinadas', [])
    letras_incorrectas = session.get('letras_incorrectas', [])
    intentos = session.get('intentos', 0)
    
    # Validar que sea una letra válida y no se haya adivinado
    if not letra.isalpha() or len(letra) != 1:
        return jsonify({'error': 'Ingresa una letra válida'}), 400
    
    if letra in letras_adivinadas or letra in letras_incorrectas:
        return jsonify({'error': 'Ya adivinaste esa letra'}), 400
    
    # Verificar si la letra está en la palabra
    if letra in palabra_secreta:
        if letra not in letras_adivinadas:
            letras_adivinadas.append(letra)
            session['letras_adivinadas'] = letras_adivinadas
    else:
        if letra not in letras_incorrectas:
            letras_incorrectas.append(letra)
            session['letras_incorrectas'] = letras_incorrectas
            intentos += 1
            session['intentos'] = intentos
    
    # Verificar si ganó o perdió
    palabra_mostrada = ''.join(
        [let if let in session['letras_adivinadas'] else '_' 
         for let in palabra_secreta]
    )
    gano = '_' not in palabra_mostrada
    perdio = intentos >= len(HANGMAN_STATES) - 1
    
    return jsonify({
        'sucess': True,
        'letra': letra,
        'gano': gano,
        'perdio': perdio
    })


@app.route('/api/nuevo_juego', methods=['POST'])
def nuevo_juego():
    """Inicia un nuevo juego"""
    iniciar_nuevo_juego()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
