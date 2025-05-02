import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter

# 1. Leer el archivo de texto
def leer_archivo(ruta):
    with open(ruta, 'r') as file:
        return file.read()

# 2. Preprocesamiento del texto: eliminar caracteres no deseados
def preprocesar_texto(texto):
    texto = texto.lower()
    texto = ''.join([c if c.isalnum() or c.isspace() else ' ' for c in texto])
    return texto

# 3. Contar las palabras
def contar_palabras(texto):
    palabras = texto.split()
    contador = Counter(palabras)
    return contador

# 4. Generar un gráfico de barras con las palabras más comunes
def generar_grafico(contador):
    palabras_comunes = contador.most_common(10)
    palabras = [x[0] for x in palabras_comunes]
    cantidades = [x[1] for x in palabras_comunes]

    plt.figure(figsize=(10,6))
    plt.barh(palabras, cantidades, color='skyblue')
    plt.xlabel('Frecuencia')
    plt.title('Top 10 palabras más comunes')
    plt.gca().invert_yaxis()
    plt.show()

# 5. Función principal para ejecutar el script
def main():
    # Ruta del archivo de texto
    ruta = 'path_to_your_text_file.txt'  # Actualiza esta ruta
    texto = leer_archivo(ruta)
    texto_procesado = preprocesar_texto(texto)
    contador = contar_palabras(texto_procesado)
    generar_grafico(contador)

# Llamar a la función principal
if __name__ == "__main__":
    main()
