from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from modules.configuracion import CONFIG


def _mostrar_imagen(ruta: str, caption: str) -> None:
    archivo = Path(ruta)
    if archivo.exists():
        st.image(str(archivo), caption=caption, use_container_width=True)
    else:
        st.info(f"Imagen pendiente: {ruta}")


def mostrar_informacion_inmueble() -> None:
    st.title(CONFIG.titulo)

    st.success(
        "Gracias por su interés. Revise las características, condiciones y "
        "ubicación antes de completar la solicitud."
    )

    _mostrar_imagen(
        CONFIG.imagen_fachada,
        "Propiedad ubicada en Higuito Centro",
    )
    _mostrar_imagen(
        CONFIG.imagen_caracteristicas,
        "Características y servicios del inmueble",
    )

    st.subheader("Características y servicios")
    st.markdown("""
    ### Características 

    - 1 Sala / Comedor
    - 1 Cocina
    - 1 Cuarto de Pilas
    - 3 Dormitorios
    - 1 Baño
    - 1 Espacio de parqueo

    #### Servicios disponibles

    - Electricidad *
    - Agua potable *
    - Internet  *

    \\* Los servicios estan incluidos dentro del pago de la mensualidad, condiciones de uso y la responsabilidad por el pago de excedentes de estos servicios se establecerán en el contrato de arrendamiento.
""")





    st.subheader("Ubicación")
    components.iframe(CONFIG.mapa_url, height=450, scrolling=False)

    st.subheader("Recorrido en video")
    st.video(CONFIG.video_url)

    st.warning(
        "Completar la solicitud no constituye aceptación, reserva ni promesa "
        "de arrendamiento."
    )

    st.divider()

    st.subheader("💰 Condiciones de alquiler")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Alquiler habitacional", CONFIG.alquiler_habitacional)
    with col2:
        st.metric("Depósito de garantía", CONFIG.deposito)

    st.info(
        "El monto indicado corresponde al uso habitacional. "
        "Las condiciones para uso comercial o mixto deben evaluarse y negociarse."
    )
