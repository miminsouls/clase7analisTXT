import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="📊 Analizador de Texto Inteligente",
    page_icon="🧠",
    layout="wide"
)

# Encabezado principal
st.markdown("""
<style>
h1, h2, h3 {
    color: #1f4e79;
}
div.stButton > button {
    background-color: #1f77b4;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Analizador de Texto con TextBlob")
st.markdown("""
Bienvenido al **Analizador de Texto Inteligente**, una herramienta interactiva que:
- 📌 Traduce tu texto de español a inglés automáticamente
- 💬 Analiza sentimientos y subjetividad con [TextBlob](https://textblob.readthedocs.io/en/dev/)
- 🔍 Extrae palabras clave y su frecuencia
- 🌐 Muestra la traducción y comparaciones frase por frase

Ideal para estudiantes, investigadores, redactores y entusiastas del análisis textual.
""")

# Opciones de entrada
st.sidebar.title("⚙️ Opciones de entrada")
modo = st.sidebar.radio("¿Cómo deseas introducir el texto?", ["📋 Escribir directamente", "📂 Subir archivo .txt"])

# Stopwords básicas (ES + EN)
stop_words = set("""
a al de el la los las y en con por para que es un una unos unas como del no sí yo tú él ella nos vos ellos ellas mi mis su sus te se lo 
do does is are am the of on in to by and an this that was were be have has had not or it at from but with they you he she we i
""".split())

# Función para contar palabras
def contar_palabras(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    conteo = {}
    for p in palabras_filtradas:
        conteo[p] = conteo.get(p, 0) + 1
    return dict(sorted(conteo.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas

# Traductor
translator = Translator()

def traducir(texto):
    try:
        return translator.translate(texto, src='es', dest='en').text
    except Exception as e:
        st.error(f"❌ Error de traducción: {e}")
        return texto

# Procesamiento
def analizar_texto(texto):
    original = texto
    traducido = traducir(original)
    blob = TextBlob(traducido)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity

    frases_es = [f.strip() for f in re.split(r'[.!?]+', original) if f.strip()]
    frases_en = [f.strip() for f in re.split(r'[.!?]+', traducido) if f.strip()]
    frases_combinadas = [{
        "original": frases_es[i],
        "traducido": frases_en[i]
    } for i in range(min(len(frases_es), len(frases_en)))]

    contador, _ = contar_palabras(traducido)

    return {
        "original": original,
        "traducido": traducido,
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador": contador
    }

# Visualizaciones
def mostrar_resultados(datos):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Sentimiento")
        valor = (datos["sentimiento"] + 1) / 2
        st.progress(valor)
        if datos["sentimiento"] > 0.05:
            st.success(f"Resultado positivo ({datos['sentimiento']:.2f})")
        elif datos["sentimiento"] < -0.05:
            st.error(f"Resultado negativo ({datos['sentimiento']:.2f})")
        else:
            st.info(f"Resultado neutral ({datos['sentimiento']:.2f})")

    with col2:
        st.subheader("💭 Subjetividad")
        st.progress(datos["subjetividad"])
        if datos["subjetividad"] > 0.5:
            st.warning(f"Subjetivo ({datos['subjetividad']:.2f})")
        else:
            st.info(f"Objetivo ({datos['subjetividad']:.2f})")

    st.markdown("---")

    st.subheader("🔠 Traducción")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Texto original (ES):**")
        st.text_area("Original", datos["original"], height=200, disabled=True)
    with col2:
        st.markdown("**Texto traducido (EN):**")
        st.text_area("Traducido", datos["traducido"], height=200, disabled=True)

    st.markdown("---")
    st.subheader("📌 Palabras más frecuentes")
    top10 = dict(list(datos["contador"].items())[:10])
    if top10:
        st.bar_chart(top10)
    else:
        st.info("No se encontraron palabras significativas.")

    st.markdown("---")
    st.subheader("📚 Traducción frase por frase")
    for par in datos["frases"]:
        st.markdown(f"➡️ *{par['original']}* → **{par['traducido']}**")

# Entrada de texto
texto = ""
if modo.startswith("📋"):
    texto = st.text_area("✍️ Escribe tu texto en español:", height=300)
else:
    archivo = st.file_uploader("📤 Sube un archivo de texto (.txt)", type="txt")
    if archivo:
        texto = archivo.read().decode("utf-8")

# Botón de análisis
if texto:
    st.markdown("### 🧪 Resultados del análisis")
    resultados = analizar_texto(texto)
    mostrar_resultados(resultados)
else:
    st.info("Introduce o sube un texto para comenzar.")
