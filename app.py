import streamlit as st
from PIL import Image

# Agregar título con emoji
st.title("📝 Análisis de Texto - Clase 7")

# Subtítulo decorativo
st.markdown("¡Bienvenid@! ✨ Esta app te permite cargar un archivo de texto y ver su contenido en pantalla.")

# Imagen decorativa opcional
# Asegúrate de tener 'imagen.jpg' en tu carpeta o comenta esta línea si no la quieres
# image = Image.open("imagen.jpg")
# st.image(image, caption="✨ Explorando textos ✨", use_column_width=True)

# Uploader con emoji
uploaded_file = st.file_uploader("📂 Sube tu archivo de texto (.txt)", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    
    st.subheader("📄 Texto cargado:")
    st.write(text)
