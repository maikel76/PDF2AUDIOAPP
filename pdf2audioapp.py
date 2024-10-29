pip install streamlit PyPDF2 pyttsx3
import streamlit as st
from PyPDF2 import PdfReader
import pyttsx3
import os

# Crea un directorio temporal si no existe
temp_dir = "temp"
os.makedirs(temp_dir, exist_ok=True)

st.title("Convertidor de PDF a Audio")

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

def pdf_to_audio(pdf_path, language="es-ES"):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""  # Asegúrate de que no haya None

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Selecciona la voz en español si está disponible
    for voice in voices:
        if "Spanish" in voice.name:
            engine.setProperty('voice', voice.id)
            break
    else:
        st.warning("No se encontró voz en español, se utilizará la voz predeterminada.")

    audio_file_path = os.path.join(temp_dir, "audio.mp3")
    engine.save_to_file(text, audio_file_path)
    engine.runAndWait()
    
    return audio_file_path

if uploaded_file is not None:
    # Guarda el archivo PDF subido
    pdf_path = os.path.join(temp_dir, uploaded_file.name)
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Convierte el PDF a audio
    audio_path = pdf_to_audio(pdf_path)
    
    # Proporciona un enlace para descargar el archivo de audio
    with open(audio_path, "rb") as f:
        st.download_button("Descargar Audio", data=f, file_name="audio.mp3")

