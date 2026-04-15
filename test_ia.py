#!/usr/bin/env python3
"""
Script de prueba para verificar la generación de palabras con IA
"""
import os
import sys
sys.path.append(os.path.dirname(__file__))

from app import generar_palabra_con_ia

print("🎮 Probando generación de palabras con IA para el Ahorcadito")
print("=" * 50)

palabras_generadas = []
for i in range(10):
    palabra = generar_palabra_con_ia()
    palabras_generadas.append(palabra)
    print(f"Palabra {i+1}: {palabra} ({len(palabra)} letras)")

print("\n" + "=" * 50)
print(f"Total de palabras generadas: {len(palabras_generadas)}")
print(f"Palabras únicas: {len(set(palabras_generadas))}")
print(f"Longitudes: {sorted([len(p) for p in palabras_generadas])}")

if len(set(palabras_generadas)) > 1:
    print("✅ ¡La IA está generando palabras variadas!")
else:
    print("⚠️  Las palabras generadas son muy similares")