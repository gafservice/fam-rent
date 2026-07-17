from datetime import date, datetime
from typing import Any

import streamlit as st
from supabase import Client, create_client


def obtener_cliente() -> Client:
    try:
        url = st.secrets["supabase"]["url"]
        secret_key = st.secrets["supabase"]["secret_key"]
    except KeyError as error:
        raise RuntimeError(
            "Falta configurar la sección [supabase] en Streamlit Secrets."
        ) from error

    if not url or not secret_key:
        raise RuntimeError(
            "La URL o la clave secreta de Supabase están vacías."
        )

    return create_client(url, secret_key)


def _convertir_a_json(valor: Any) -> Any:
    if isinstance(valor, (date, datetime)):
        return valor.isoformat()

    if isinstance(valor, dict):
        return {
            clave: _convertir_a_json(contenido)
            for clave, contenido in valor.items()
        }

    if isinstance(valor, (list, tuple, set)):
        return [_convertir_a_json(elemento) for elemento in valor]

    return valor


def guardar_solicitud(datos: dict[str, Any]) -> dict[str, Any]:
    cliente = obtener_cliente()
    datos_json = _convertir_a_json(datos)

    registro = {
        "numero_solicitud": datos["Número de solicitud"],
        "fecha_envio": datos["Fecha de envío"],
        "tipo_uso": datos["Tipo de uso"],
        "nombre_completo": datos["Nombre completo"],
        "identificacion": datos["Identificación"],
        "telefono_principal": datos["Teléfono principal"],
        "correo_electronico": datos["Correo electrónico"],
        "estado": "recibida",
        "datos": datos_json,
    }

    respuesta = (
        cliente
        .table("solicitudes")
        .insert(registro)
        .execute()
    )

    if not respuesta.data:
        raise RuntimeError(
            "Supabase no devolvió información del registro insertado."
        )

    return respuesta.data[0]