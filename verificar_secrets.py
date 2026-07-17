import streamlit as st

st.title("Verificación de Secrets")

st.write("Secciones encontradas:", list(st.secrets.keys()))

if "supabase" in st.secrets:
    st.success("La sección [supabase] existe.")
    st.write("Claves encontradas:", list(st.secrets["supabase"].keys()))
else:
    st.error("La sección [supabase] no existe.")
