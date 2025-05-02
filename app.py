import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Texto Simple",
    page_icon="📊",
    layout="wide"
)

# Título y descripción
st.title("📝 Analizador de Texto con TextBlob")
st.markdown("""
Esta aplicación utiliza TextBlob para realizar un análisis básico de texto:
- Análisis de sentimiento y subjetividad
- Extracción de palabras clave
- Análisis de frecuencia de palabras
""")

# Mostrar imagen decorativa
st.image("imagen_decorativa.jpg", use_column_width=True)

# Barra lateral
st.sidebar.title("Opciones")
modo = st.sidebar.selectbox(
    "Selecciona el modo de entrada:",
    ["Texto directo", "Archivo de texto"]
)

# Función para contar palabras sin depender de NLTK
def contar_palabras(texto):
    stop_words = set([
        # Lista de palabras vacías en español e inglés
        "a", "al", "algo", "algunas", "algunos", "ante", "antes", "como", "con", "contra",
        "cual", "cuando", "de", "del", "desde", "donde", "durante", "e", "el", "ella",
        "ellas", "ellos", "en", "entre", "era", "eras", "es", "esa", "esas", "ese",
        "eso", "esos", "esta", "estas", "este", "esto", "estos", "ha", "había", "han",
        "has", "hasta", "he", "la", "las", "le", "les", "lo", "los", "me", "mi", "mía",
        "mías", "mío", "míos", "mis", "mucho", "muchos", "muy", "nada", "ni", "no", "nos",
        "nosotras", "nosotros", "nuestra", "nuestras", "nuestro", "nuestros", "o", "os", 
        "otra", "otras", "otro", "otros", "para", "pero", "poco", "por", "porque", "que", 
        "quien", "quienes", "qué", "se", "sea", "sean", "según", "si", "sido", "sin", 
        "sobre", "sois", "somos", "son", "soy", "su", "sus", "suya", "suyas", "suyo", 
        "suyos", "también", "tanto", "te", "tenéis", "tenemos", "tener", "tengo", "ti", 
        "tiene", "tienen", "todo", "todos", "tu", "tus", "tuya", "tuyas", "tuyo", "tuyos", 
        "tú", "un", "una", "uno", "unos", "vosotras", "vosotros", "vuestra", "vuestras", 
        "vuestro", "vuestros", "y", "ya", "yo",
        # Inglés
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", 
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", 
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", 
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", 
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", 
        "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", 
        "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", 
        "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", 
        "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", 
        "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", 
        "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", 
        "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", 
        "the", "their", "theirs", "them", "themselves", "then", "there", "there's", 
        "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", 
        "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", 
        "we'd", "we'll", "we're", "we've", "were",         "weren't", "what", "what's", "when", 
        "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", 
        "why's", "with", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
        "your", "yours", "yourself", "yourselves"
    ])
    
    # Limpiar y tokenizar texto
    palabras = re.findall(r'\b\w+\b', texto.lower())
    
    # Filtrar palabras vacías y contar frecuencias
    palabras_filtradas = [palabra for palabra in palabras 
                         if palabra not in stop_words and len(palabra) > 2]
    
    # Contar frecuencias
    contador = {}
    for palabra in palabras_filtradas:
        contador[palabra] = contador.get(palabra, 0) + 1
    
    # Ordenar por frecuencia
    contador_ordenado = dict(sorted(contador.items(), key=lambda x: x[1], reverse=True))
    
    return contador_ordenado, palabras_filtradas

# Inicializar el traductor
translator = Translator()

# Función para traducir texto del español al inglés
def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"Error al traducir: {e}")
        return texto  # Devolver el texto original si falla la traducción

# Función para procesar el texto con TextBlob (versión con traducción)
def procesar_texto(texto):
    # Guardar el texto original
    texto_original = texto
    
    # Traducir el texto al inglés para mejor análisis
    texto_ingles = traducir_texto(texto)
    
    # Analizar el texto traducido con TextBlob
    blob = TextBlob(texto_ingles)
    
    # Análisis de sentimiento (esto no requiere corpus adicionales)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    
    # Extraer frases de manera simplificada (del texto original)
    frases_originales = [frase.strip() for frase in re.split(r'[.!?]+', texto_original) if frase.strip()]
    
    # Extraer frases del texto traducido
    frases_traducidas = [frase.strip() for frase in re.split(r'[.!?]+', texto_ingles) if frase.strip()]
    
    # Combinar frases originales y traducidas
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({
            "original": frases_originales[i],
            "traducido": frases_traducidas[i]
        })
    
    # Contar palabras con nuestra función simplificada (en el texto traducido)
    contador_palabras, palabras = contar_palabras(texto_ingles)
    
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

# Función para crear visualizaciones usando componentes nativos de Streamlit
def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    
    # Visualización de sentimiento y subjetividad con barras de progreso de Streamlit
    with col1:
        st.markdown("### Sentimiento")
        st.progress(int((resultados["sentimiento"] + 1) * 50))  # Sentimiento en -1 a 1, ajustado a 0-100
    
    with col2:
        st.markdown("### Subjetividad")
        st.progress(int(resultados["subjetividad"] * 100))  # Subjetividad de 0 a 1, ajustado a 0-100
    
    # Visualización de la frecuencia de palabras
    st.markdown("### Frecuencia de palabras más comunes")
    for palabra, frecuencia in resultados["contador_palabras"].items():
        st.write(f"{palabra}: {frecuencia} veces")

# Función para cargar un archivo de texto
def cargar_archivo():
    archivo = st.file_uploader("Sube un archivo de texto", type=["txt"])
    if archivo is not None:
        texto = archivo.read().decode("utf-8")
        return texto
    return ""

# Función para mostrar la entrada de texto o archivo
def procesar_entrada():
    texto = ""
    if modo == "Texto directo":
        texto = st.text_area("Escribe tu texto aquí", height=250)
    elif modo == "Archivo de texto":
        texto = cargar_archivo()

    if texto:
        resultados = procesar_texto(texto)
        crear_visualizaciones(resultados)

# Procesar entrada y mostrar resultados
procesar_entrada()
