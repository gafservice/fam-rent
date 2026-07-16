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

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Alquiler habitacional", CONFIG.alquiler_habitacional)
    with col2:
        st.metric("Depósito de garantía", CONFIG.deposito)

    st.subheader("Características y servicios")
    st.markdown(
        """
        - 1 sala / comedor
        - 1 cocina, sin electrodomésticos
        - 3 dormitorios
        - 1 baño con agua caliente
        - 1 cuarto de pilas, sin lavadora
        - 1 espacio de parqueo
        - Electricidad y agua potable disponibles
        - Internet y TV Kolbi disponibles
        - Se permiten mascotas bajo tenencia responsable
        """
    )

    st.info(
        "El monto indicado corresponde al uso habitacional. "
        "Las condiciones para uso comercial o mixto deben evaluarse y negociarse."
    )

    st.subheader("Ubicación")
    components.iframe(CONFIG.mapa_url, height=450, scrolling=False)

    st.subheader("Recorrido en video")
    st.video(CONFIG.video_url)

    st.warning(
        "Completar la solicitud no constituye aceptación, reserva ni promesa "
        "de arrendamiento."
    )
