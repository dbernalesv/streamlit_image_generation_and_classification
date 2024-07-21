import streamlit as st
import transformers
import torch
from diffusers import StableDiffusionPipeline
from utils import generate_images, recognition_images
from PIL import Image
import numpy as np
import io

# Agregar estilo CSS para separar las columnas con una línea vertical de color fucsia
st.markdown(
    """
    <style>
    .custom-separator {
        border-left: 2px solid #87CEFA; /* Color azul claro */
        height: 100%; /* Ajustar la altura de la línea */
        margin-left: 1rem; /* Ajustar el margen izquierdo para separar las secciones */
        margin-right: 1rem; /* Ajustar el margen derecho para separar las secciones */
        padding-left: 1rem; /* Añadir relleno a la izquierda para separar visualmente */
        padding-right: 1rem; /* Añadir relleno a la derecha para separar visualmente */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# URL del logo de Hugging Face
hugging_face_logo_url = "https://huggingface.co/front/assets/huggingface_logo.svg"

# Mostrar el logo de Hugging Face en la esquina superior derecha desde la URL
st.image(hugging_face_logo_url, width=50)

# Establecer el título de la aplicación web en Streamlit
st.title("Image Generation and Recognition Streamlit app")
# Mostrar un mensaje de texto en la aplicación
st.write("Diego Bernales")

choice = st.sidebar.selectbox("Selecciona: ", ["Generar Imágenes", "Reconocer Imágenes"])

if choice == "Generar Imágenes":

    # Crear un contenedor en Streamlit para organizar los elementos de la interfaz
    with st.container():
        # Crear dos columnas en la interfaz
        col1, col_separator, col2 = st.columns([10, 0.5, 10])

        with col1:
            st.subheader("Image generation:")
            input_prompt = st.text_input("Ingresa tu petición y presiona Enter")

            st.write("Seleccionar la siguiente opción para reconocer automáticamente el ouput del modelo:")

            auto_predict = st.checkbox("Reconocimiento automático")
    
            if input_prompt is not None:
                if st.button("Generate Image"):
                    image_output = generate_images(input_prompt)
                    st.info("Generating image.....")
                    st.success("Image Generated Successfully")
                    st.image(image_output)

                    buf = io.BytesIO()
                    image_output.save(buf, format="PNG")
                    byte_im = buf.getvalue()

                    btn = st.download_button(
                        label="Descargar imagen",
                        data=byte_im,
                        file_name="image.png",
                        mime="image/png"
                        )
                    
                    if auto_predict:
                        with col_separator:
                            st.markdown('<hr class="custom-separator" style="height: 100vh;">', unsafe_allow_html=True)

                        with col2:
                            st.info("Reconociendo imagen automáticamente...")
                            prediccion = recognition_images(image_output)
                            st.success("Reconocimiento completo")
                            st.write(f"Se observa en la imagen generada: ")
                            st.write(" ")
                            st.write(f"{prediccion}")
            else:
                st.write("Ingresa una petición")

elif choice == "Reconocer Imágenes":

    st.subheader("Reconocimiento de imagenes:")
        
    uploaded_file = st.file_uploader("Choose a image file", type=['jpg', 'png'])
            
    if uploaded_file is not None:

        uploaded_file = Image.open(uploaded_file)
        st.image(uploaded_file)
        st.write("Imagen Cargada Correctamente")

        if st.button("Reconocer Imagen"):
            prediccion = recognition_images(uploaded_file)
            st.info("Reconociendo imagen.....")
            st.success("Reconocimiento completo")
            st.write(f"Se observa en la imagen generada: ")
            st.write(" ")
            st.write(f"{prediccion}")
        else:
            st.write("Make sure you image is in JPG/PNG Format.")
