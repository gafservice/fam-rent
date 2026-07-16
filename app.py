import streamlit as st

from modules.formulario import mostrar_formulario
from modules.inmueble import mostrar_informacion_inmueble

st.set_page_config(
    page_title="Casa en alquiler - Higuito Centro",
    page_icon="🏡",
    layout="centered",
)

mostrar_informacion_inmueble()
mostrar_formulario()
