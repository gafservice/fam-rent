from typing import Any

import streamlit as st

from modules.configuracion import CONFIG
from modules.correo import enviar_correos
from modules.supabase_db import guardar_solicitud
from modules.utilidades import (
    fecha_actual_costa_rica,
    fecha_hora_costa_rica,
    generar_numero_solicitud,
)
from modules.validaciones import (
    campos_obligatorios_faltantes,
    normalizar_telefono,
    validar_correo,
    validar_telefono,
)


CAMPOS_OBLIGATORIOS = [
    "Nombre completo",
    "Identificación",
    "Teléfono principal",
    "Correo electrónico",
    "Profesión u ocupación",
    "Ingreso mensual aproximado",
    "Fecha prevista de ingreso",
]


def _normalizar_identificacion_contacto(datos: dict[str, Any]) -> None:
    datos["Nombre completo"] = " ".join(
        datos["Nombre completo"].split()
    )
    datos["Identificación"] = datos["Identificación"].strip()
    datos["Correo electrónico"] = (
        datos["Correo electrónico"].strip().lower()
    )


def _seccion_identificacion(datos: dict[str, Any]) -> None:
    st.subheader("1. Identificación y contacto")

    datos["Nombre completo"] = st.text_input("Nombre completo *")
    datos["Identificación"] = st.text_input(
        "Número de cédula, DIMEX o pasaporte *"
    )
    datos["Mayor de edad"] = st.radio(
        "¿Es mayor de 18 años?",
        ["Sí", "No"],
        horizontal=True,
    )
    datos["Teléfono principal"] = st.text_input("Teléfono principal *")
    datos["Teléfono alternativo"] = st.text_input("Teléfono alternativo")
    datos["Correo electrónico"] = st.text_input("Correo electrónico *")
    datos["Medio preferido de contacto"] = st.radio(
        "Medio preferido de contacto",
        ["Teléfono", "WhatsApp", "Correo electrónico"],
        horizontal=True,
    )


def _seccion_economica(datos: dict[str, Any]) -> None:
    st.subheader("2. Situación laboral y económica")

    datos["Profesión u ocupación"] = st.text_input(
        "Profesión u ocupación *"
    )
    datos["Empresa o actividad"] = st.text_input(
        "Empresa donde trabaja o actividad independiente"
    )
    datos["Puesto"] = st.text_input("Puesto desempeñado")
    datos["Antigüedad laboral"] = st.text_input(
        "Tiempo de laborar o ejercer la actividad"
    )
    datos["Ingreso mensual aproximado"] = st.number_input(
        "Ingreso mensual aproximado (₡) *",
        min_value=0,
        value=None,
        step=10_000,
        format="%d",
        placeholder="Ejemplo: 500000",
    )
    datos["Otros ingresos"] = st.number_input(
        "Otros ingresos mensuales verificables (₡)",
        min_value=0,
        value=None,
        step=10_000,
        format="%d",
        placeholder="Opcional",
    )
    datos["Comprobante de ingresos"] = st.multiselect(
        "Documentos que podría presentar si es preseleccionado",
        [
            "Constancia salarial",
            "Orden patronal",
            "Estados de cuenta",
            "Certificación de ingresos",
            "Declaraciones tributarias",
            "Otro",
        ],
    )
    datos["Fecha prevista de ingreso"] = st.date_input(
        "Fecha prevista para ingresar *",
        value=None,
        min_value=fecha_actual_costa_rica(),
        format="DD/MM/YYYY",
    )
    datos["Plazo previsto de alquiler"] = st.selectbox(
        "¿Por cuánto tiempo espera alquilar?",
        [
            "Menos de 1 año",
            "1 año",
            "Entre 1 y 2 años",
            "Más de 2 años",
        ],
    )


def _seccion_ocupantes(datos: dict[str, Any]) -> None:
    st.subheader("3. Personas que ocuparán la vivienda")

    datos["Cantidad de ocupantes"] = st.number_input(
        "Cantidad total de ocupantes",
        min_value=1,
        step=1,
    )
    datos["Adultos"] = st.text_area(
        "Nombres y edades de las personas adultas"
    )
    datos["Menores y edades"] = st.text_area(
        "Cantidad de menores y sus edades"
    )
    datos["Relación entre ocupantes"] = st.text_area(
        "Relación entre las personas que vivirán en la casa"
    )
    datos["Trabajo desde la vivienda"] = st.radio(
        "¿Alguna persona trabajará regularmente desde la vivienda?",
        ["Sí", "No"],
        horizontal=True,
    )


def _seccion_mascotas_vehiculos(datos: dict[str, Any]) -> None:
    st.subheader("4. Mascotas y vehículos")

    datos["Mascotas"] = st.radio(
        "¿Tiene mascotas?",
        ["Sí", "No"],
        horizontal=True,
    )
    if datos["Mascotas"] == "Sí":
        datos["Detalle de mascotas"] = st.text_area(
            "Tipo, raza, cantidad, tamaño y edad de las mascotas"
        )
        datos["Tenencia responsable"] = st.checkbox(
            "Acepto responder por cualquier daño causado por mis mascotas."
        )
    else:
        datos["Detalle de mascotas"] = ""
        datos["Tenencia responsable"] = False

    datos["Cantidad de vehículos"] = st.number_input(
        "Cantidad de vehículos",
        min_value=0,
        step=1,
    )
    datos["Necesita parqueo adicional"] = st.radio(
        "¿Necesita más de un espacio de parqueo? "
        "(Seleccione No si tiene cero o un vehículo)",
        ["Sí", "No"],
        horizontal=True,
    )


def _seccion_historial(datos: dict[str, Any]) -> None:
    st.subheader("5. Historial de alquiler y referencias")

    datos["Actualmente alquila"] = st.radio(
        "¿Actualmente alquila otra propiedad?",
        ["Sí", "No"],
        horizontal=True,
    )
    datos["Zona del alquiler anterior"] = st.text_input(
        "Zona o dirección general del alquiler anterior"
    )
    datos["Tiempo en alquiler anterior"] = st.text_input(
        "Tiempo que permaneció en el alquiler anterior"
    )
    datos["Motivo de salida"] = st.text_area(
        "Motivo por el que dejó o dejará el lugar anterior"
    )
    datos["Propietario anterior"] = st.text_input(
        "Nombre del propietario o administrador anterior"
    )
    datos["Contacto propietario anterior"] = st.text_input(
        "Teléfono o correo del propietario anterior"
    )
    datos["Referencia laboral"] = st.text_input(
        "Nombre de referencia laboral"
    )
    datos["Teléfono referencia laboral"] = st.text_input(
        "Teléfono de referencia laboral"
    )
    datos["Referencia personal"] = st.text_input(
        "Nombre de referencia personal"
    )
    datos["Teléfono referencia personal"] = st.text_input(
        "Teléfono de referencia personal"
    )


def _seccion_condiciones(datos: dict[str, Any]) -> None:
    st.subheader("6. Condiciones generales")

    st.info(
        f"Alquiler mensual: {CONFIG.alquiler_habitacional}. "
        f"Depósito de garantía: {CONFIG.deposito}. "
        "El primer mes se paga antes de ingresar. La mensualidad incluye "
        "internet y un consumo base de agua y electricidad. Si se supera "
        "la base establecida, se cobrará al inquilino el 80 % del monto "
        "excedente. Las bases, el cálculo y las demás condiciones se "
        "detallarán en el contrato."
    )

    datos["Valoración de condiciones"] = st.radio(
        "Después de revisar esta información:",
        [
            "Las condiciones me resultan viables",
            "Necesito conversar algunas condiciones",
            "Las condiciones no se ajustan a mi situación",
        ],
        index=None,
    )

    datos["Condición por conversar"] = st.text_area(
        "Condición u observación que desea conversar (opcional)"
    )

def _seccion_privacidad(datos: dict[str, Any]) -> None:
    st.subheader("7. Declaraciones y consentimiento")

    st.info(
        "Los datos se utilizarán únicamente para evaluar esta solicitud, "
        "verificar referencias y contactar al oferente. Si no se formaliza "
        "el alquiler, se eliminarán en un plazo máximo de 15 días, salvo "
        "obligación legal de conservación."
    )

    datos["Declaración de veracidad"] = st.checkbox(
        "Declaro que la información suministrada es verdadera y completa."
    )
    datos["Autorización de verificación"] = st.checkbox(
        "Autorizo verificar las referencias indicadas."
    )
    datos["Consentimiento de datos"] = st.checkbox(
        "Autorizo el tratamiento de mis datos para evaluar esta solicitud."
    )


def mostrar_formulario() -> None:
    st.divider()
    st.header("Solicitud de alquiler")

    st.write(
        "Complete la información con datos verdaderos. Los campos marcados "
        "con * son obligatorios."
    )

    with st.form("solicitud_alquiler", clear_on_submit=False):
        datos: dict[str, Any] = {}

        datos["Tipo de uso"] = st.radio(
            "Uso solicitado",
            ["Habitacional", "Comercial", "Mixto"],
            horizontal=True,
        )

        _seccion_identificacion(datos)
        _seccion_economica(datos)
        _seccion_ocupantes(datos)
        _seccion_mascotas_vehiculos(datos)
        _seccion_historial(datos)
        _seccion_condiciones(datos)
        _seccion_privacidad(datos)

        archivo = st.file_uploader(
            "Documento opcional de respaldo",
            type=["pdf", "jpg", "jpeg", "png"],
        )

        enviado = st.form_submit_button(
            "Enviar solicitud",
            type="primary",
            use_container_width=True,
        )

    if not enviado:
        return

    _normalizar_identificacion_contacto(datos)

    faltantes = campos_obligatorios_faltantes(
        datos,
        CAMPOS_OBLIGATORIOS,
    )

    if faltantes:
        st.error(
            "Complete los siguientes campos obligatorios: "
            + ", ".join(faltantes)
        )
        return

    if datos["Ingreso mensual aproximado"] <= 0:
        st.error("El ingreso mensual aproximado debe ser mayor que cero.")
        return

    if datos["Mascotas"] == "Sí":
        if not datos["Detalle de mascotas"].strip():
            st.error(
                "Describa el tipo, cantidad, tamaño y edad de las mascotas."
            )
            return
        if not datos["Tenencia responsable"]:
            st.error(
                "Debe aceptar la responsabilidad por los daños que puedan "
                "causar sus mascotas."
            )
            return

    if datos["Cantidad de vehículos"] <= 1:
        datos["Necesita parqueo adicional"] = "No"

    if datos["Mayor de edad"] != "Sí":
        st.error("La persona responsable del contrato debe ser mayor de edad.")
        return

    if not validar_correo(datos["Correo electrónico"]):
        st.error("Ingrese una dirección de correo electrónico válida.")
        return

    if not validar_telefono(datos["Teléfono principal"]):
        st.error(
            "Ingrese un teléfono válido de Costa Rica con 8 dígitos. "
            "Puede escribirlo como 8888-8888 o +506 8888-8888."
        )
        return

    datos["Teléfono principal"] = normalizar_telefono(
        datos["Teléfono principal"]
    )

    if datos["Teléfono alternativo"]:
        if not validar_telefono(datos["Teléfono alternativo"]):
            st.error(
                "El teléfono alternativo debe tener 8 dígitos o dejarse vacío."
            )
            return
        datos["Teléfono alternativo"] = normalizar_telefono(
            datos["Teléfono alternativo"]
        )

    consentimientos_obligatorios = [
    datos["Declaración de veracidad"],
    datos["Consentimiento de datos"],
]

    if not all(consentimientos_obligatorios):
        st.error(
        "Debe aceptar la declaración de veracidad y el consentimiento "
        "para el tratamiento de datos."
    )
    return

    proporciono_referencias = any(
    [
        datos["Propietario anterior"].strip(),
        datos["Contacto propietario anterior"].strip(),
        datos["Referencia laboral"].strip(),
        datos["Teléfono referencia laboral"].strip(),
        datos["Referencia personal"].strip(),
        datos["Teléfono referencia personal"].strip(),
    ]
    )

    if proporciono_referencias and not datos["Autorización de verificación"]:
        st.error(
        "Para utilizar las referencias proporcionadas, debe autorizar "
        "su verificación."
    )
    return

    datos["Número de solicitud"] = generar_numero_solicitud()
    datos["Fecha de envío"] = fecha_hora_costa_rica()

    try:
        guardar_solicitud(datos)
    except Exception:
        st.error(
            "No fue posible guardar la solicitud. "
            "Por favor, inténtelo nuevamente."
        )
        return

    try:
        enviar_correos(
            datos,
            datos["Correo electrónico"],
            archivo,
        )
    except Exception:
        st.warning(
            "La solicitud fue registrada, pero no fue posible enviar "
            "el correo de confirmación."
        )

    st.success(
        f"Solicitud enviada correctamente. "
        f"Número de seguimiento: {datos['Número de solicitud']}"
    )