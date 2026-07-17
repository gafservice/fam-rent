import streamlit as st

from modules.supabase_db import obtener_cliente


st.title("Prueba de conexión con Supabase")

try:
    cliente = obtener_cliente()

    respuesta = (
        cliente
        .table("solicitudes")
        .select("id")
        .limit(1)
        .execute()
    )

    st.success("Conexión correcta con Supabase")
    st.write(respuesta.data)

except Exception as error:
    st.error("No fue posible conectar con Supabase")
    st.exception(error)