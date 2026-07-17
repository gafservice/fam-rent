import smtplib
import streamlit as st
from email.message import EmailMessage


st.title("Prueba SMTP")

usuario = st.secrets["email"]["usuario"]
password = st.secrets["email"]["password"]
servidor_smtp = st.secrets["email"].get(
    "smtp_server",
    "smtp.gmail.com",
)
puerto = int(st.secrets["email"].get("smtp_port", 587))

if st.button("Probar correo"):
    try:
        mensaje = EmailMessage()
        mensaje["Subject"] = "Prueba SMTP FAM-Rent"
        mensaje["From"] = usuario
        mensaje["To"] = usuario
        mensaje.set_content(
            "Esta es una prueba de correo enviada desde FAM-Rent."
        )

        with smtplib.SMTP(
            servidor_smtp,
            puerto,
            timeout=30,
        ) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(usuario, password)
            server.send_message(mensaje)

        st.success("Correo enviado correctamente.")

    except Exception as error:
        st.error("Falló la prueba SMTP.")
        st.exception(error)