import streamlit as st
import pandas as pd
from collections import Counter
from textblob import TextBlob
from googletrans import Translator
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io

st.set_page_config(page_title="Análisis de Texto", layout="wide")

st.title("📝 Análisis de Texto con IA")

modo = st.radio("Selecciona el modo de entrada:", ["Texto directo", "Archivo de texto"])

# Función de procesamiento
def procesar_texto(texto):
    blob = TextBlob(texto)
    traduccion = blob.translate(to='en')
    sentimiento = traduccion.sentiment.polarity
    subjetividad = traduccion.sentiment.subjectivity
    palabras = [word.lower() for word in blob.words if word.isalpha()]
    contador = Counter(palabras)
    return {
        "texto_original": texto,
        "texto_traducido": str(traduccion),
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "contador_palabras": contador
    }

# Función para visualizaciones
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔎 Sentimiento y Subjetividad")
        st.write("**Sentimiento (Polaridad)**", f"{resultados['sentimiento']:.2f}")
        st.progress(int((resultados['sentimiento'] + 1) * 50))  # escala 0-100
        st.write("**Subjetividad**", f"{resultados['subjetividad']:.2f}")
        st.progress(int(resultados['subjetividad'] * 100))

        # Gráfico de torta del sentimiento
        st.subheader("📊 Visualización de Sentimiento")
        labels = ['Negativo', 'Neutro', 'Positivo']
        if resultados['sentimiento'] > 0.05:
            sizes = [0, 0, 1]
        elif resultados['sentimiento'] < -0.05:
            sizes = [1, 0, 0]
        else:
            sizes = [0, 1, 0]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.0f%%', colors=['red', 'gray', 'green'])
        ax1.axis('equal')
        st.pyplot(fig1)

    with col2:
        st.subheader("🌥️ Nube de Palabras")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(resultados["contador_palabras"])
        fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
        ax_wc.imshow(wordcloud, interpolation='bilinear')
        ax_wc.axis("off")
        st.pyplot(fig_wc)

        st.subheader("📋 Top Palabras Más Comunes")
        comunes = list(resultados["contador_palabras"].items())[:10]
        df_comunes = pd.DataFrame(comunes, columns=["Palabra", "Frecuencia"])
        st.dataframe(df_comunes)

# Entrada de texto
if modo == "Texto directo":
    texto_entrada = st.text_area("✍️ Escribe o pega tu texto aquí:", height=200)
elif modo == "Archivo de texto":
    archivo = st.file_uploader("📁 Sube un archivo .txt", type="txt")
    if archivo:
        texto_entrada = archivo.read().decode("utf-8")
    else:
        texto_entrada = ""

# Procesar si hay texto
if texto_entrada:
    resultados = procesar_texto(texto_entrada)
    st.subheader("📌 Resumen del Análisis")
    st.write(f"**Texto Original:** {resultados['texto_original']}")
    st.write(f"**Texto Traducido (al inglés):** {resultados['texto_traducido']}")
    crear_visualizaciones(resultados)

# Pie de página
st.markdown("---")
st.markdown("Hecho con ❤️ por [Tu Nombre o Proyecto] • Powered by Streamlit, TextBlob y Google Translate API")
