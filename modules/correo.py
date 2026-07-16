import mimetypes
import smtplib
from email.message import EmailMessage
from typing import Any

import streamlit as st


def _configuracion_correo() -> tuple[str, str, str, int]:
    usuario = st.secrets["email"]["usuario"]
    password = st.secrets["email"]["password"]
    servidor = st.secrets["email"].get("smtp_server", "smtp.gmail.com")
    puerto = int(st.secrets["email"].get("smtp_port", 587))
    return usuario, password, servidor, puerto


def _cuerpo_resumen(datos: dict[str, Any]) -> str:
    return "\n".join(f"{clave}: {valor}" for clave, valor in datos.items())


def enviar_correos(
    datos: dict[str, Any],
    correo_interesado: str,
    archivo_adjunto=None,
) -> None:
    usuario, password, servidor_smtp, puerto = _configuracion_correo()
    resumen = _cuerpo_resumen(datos)

    mensaje_admin = EmailMessage()
    mensaje_admin["Subject"] = (
        f"Nueva solicitud de alquiler - {datos['Número de solicitud']}"
    )
    mensaje_admin["From"] = usuario
    mensaje_admin["To"] = usuario
    mensaje_admin.set_content(resumen)

    if archivo_adjunto is not None:
        mime_type, _ = mimetypes.guess_type(archivo_adjunto.name)
        if mime_type:
            maintype, subtype = mime_type.split("/", 1)
        else:
            maintype, subtype = "application", "octet-stream"

        mensaje_admin.add_attachment(
            archivo_adjunto.getvalue(),
            maintype=maintype,
            subtype=subtype,
            filename=archivo_adjunto.name,
        )

    mensaje_usuario = EmailMessage()
    mensaje_usuario["Subject"] = (
        f"Confirmación de solicitud {datos['Número de solicitud']}"
    )
    mensaje_usuario["From"] = usuario
    mensaje_usuario["To"] = correo_interesado
    mensaje_usuario.set_content(
        f"""Estimado/a {datos.get('Nombre completo', 'interesado/a')}:

Hemos recibido su solicitud de alquiler.

Número de solicitud: {datos['Número de solicitud']}
Fecha de envío: {datos['Fecha de envío']}

Completar el formulario no garantiza la aprobación ni reserva la propiedad.
La administración se comunicará con las personas preseleccionadas.

Atentamente,
Administración de Propiedades
VIGIAS
"""
    )

    with smtplib.SMTP(servidor_smtp, puerto, timeout=30) as server:
        server.starttls()
        server.login(usuario, password)
        server.send_message(mensaje_admin)
        server.send_message(mensaje_usuario)
