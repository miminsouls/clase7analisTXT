import streamlit as st
import pandas as pd
from PIL import Image

# Título con emoji
st.title("📝 Análisis de Texto - Clase 7")

# Subtítulo con estilo
st.subheader("Explorando el contenido textual con estilo 💫")

# Agregar una imagen decorativa
image = Image.open("imagen_decorativa.jpg")
st.image(image, caption="Visualización del análisis de texto", use_column_width=True)

# Texto descriptivo
st.markdown("""
¡Bienvenido a la aplicación de análisis de texto! Aquí podrás cargar tus archivos y obtener un resumen detallado de su contenido. 📄🔍

**Pasos a seguir:**
1. Sube tu archivo de texto.
2. Observa el resumen generado.
3. Disfruta de una visualización clara y concisa.

¡Comencemos! 🚀
""")

# Cargar archivo de texto
uploaded_file = st.file_uploader("Elige un archivo de texto", type=["txt"])

if uploaded_file is not None:
    # Leer el contenido del archivo
    text = uploaded_file.read().decode("utf-8")

    # Mostrar el contenido original
    st.subheader("📄 Contenido Original:")
    st.write(text)

    # Mostrar resumen (aquí puedes agregar tu lógica de resumen)
    st.subheader("🧠 Resumen del Texto:")
    st.write("Aquí se mostrará el resumen del texto cargado.")
