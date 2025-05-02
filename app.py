import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
from PIL import Image

# Configurar la página
st.set_page_config(page_title="Análisis de Texto con TextBlob", layout="wide")

# Mostrar imagen decorativa
imagen = Image.open("imagen_decorativa.jpg")
st.image(imagen, use_column_width=True)

# Título estilizado y descripción
st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>📝 Analizador de Texto con TextBlob</h1>
    <p style='text-align: center; font-size: 18px;'>Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:<br>
    - Análisis de sentimiento y subjetividad<br>
    - Extracción de palabras clave<br>
    - Análisis de frecuencia de palabras</p>
""", unsafe_allow_html=True)

# Área de entrada de texto
texto = st.text_area("Introduce el texto que quieres analizar:", height=200)

# Botón para ejecutar el análisis
if st.button("Analizar"):
    if texto.strip() == "":
        st.warning("Por favor, introduce algún texto para analizar.")
    else:
        # Crear el objeto TextBlob
        blob = TextBlob(texto)

        # Mostrar análisis de sentimiento
        st.subheader("📊 Análisis de Sentimiento")
        polaridad = blob.sentiment.polarity
        subjetividad = blob.sentiment.subjectivity

        st.write(f"**Polaridad:** {polaridad:.2f}")
        st.write(f"**Subjetividad:** {subjetividad:.2f}")

        if polaridad > 0:
            st.success("El texto tiene un sentimiento positivo.")
        elif polaridad < 0:
            st.error("El texto tiene un sentimiento negativo.")
        else:
            st.info("El texto es neutral.")

        # Palabras clave (sustantivos más comunes)
        st.subheader("🔑 Palabras Clave")
        palabras_clave = [word for word, tag in blob.tags if tag == 'NN']
        palabras_frecuentes = Counter(palabras_clave).most_common(5)

        if palabras_frecuentes:
            for palabra, frecuencia in palabras_frecuentes:
                st.write(f"- {palabra} ({frecuencia} veces)")
        else:
            st.write("No se encontraron sustantivos clave.")

        # WordCloud
        st.subheader("☁️ Nube de Palabras")
        palabras_limpias = re.findall(r'\w+', texto.lower())
        texto_limpio = " ".join(palabras_limpias)

        if texto_limpio:
            nube = WordCloud(width=800, height=400, background_color='white').generate(texto_limpio)
            fig, ax = plt.subplots()
            ax.imshow(nube, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.write("No hay suficiente contenido para generar una nube de palabras.")
