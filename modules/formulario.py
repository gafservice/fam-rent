from typing import Any

import streamlit as st

from modules.configuracion import CONFIG
from modules.correo import enviar_correos
from modules.google_sheets import guardar_solicitud
from modules.utilidades import fecha_hora_costa_rica, generar_numero_solicitud
from modules.validaciones import campos_obligatorios_faltantes, validar_correo


CAMPOS_OBLIGATORIOS = [
    "Nombre completo",
    "Identificación",
    "Teléfono principal",
    "Correo electrónico",
    "Profesión u ocupación",
    "Ingreso mensual aproximado",
    "Fecha prevista de ingreso",
]


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
    datos["Ingreso mensual aproximado"] = st.text_input(
        "Ingreso mensual aproximado (₡) *"
    )
    datos["Otros ingresos"] = st.text_input(
        "Otros ingresos mensuales verificables"
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
        "Fecha prevista para ingresar *"
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
        datos["Tenencia responsable"] = "No aplica"

    datos["Cantidad de vehículos"] = st.number_input(
        "Cantidad de vehículos",
        min_value=0,
        step=1,
    )
    datos["Necesita parqueo adicional"] = st.radio(
        "¿Necesita más de un espacio de parqueo?",
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
    datos["Autoriza contactar referencia"] = st.checkbox(
        "Autorizo contactar al propietario o administrador anterior."
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
    st.subheader("6. Condiciones de contratación")

    datos["Acepta monto de alquiler"] = st.checkbox(
        f"Acepto el alquiler mensual indicado: {CONFIG.alquiler_habitacional}."
    )
    datos["Acepta depósito"] = st.checkbox(
        f"Acepto entregar el depósito de garantía: {CONFIG.deposito}."
    )
    datos["Acepta primer mes adelantado"] = st.checkbox(
        "Acepto pagar el primer mes antes de ingresar."
    )
    datos["Acepta contrato escrito"] = st.checkbox(
        "Acepto formalizar un contrato escrito."
    )
    datos["Acepta normas de convivencia"] = st.checkbox(
        "Acepto cumplir las normas de convivencia y cuidar el inmueble."
    )
    datos["Acepta prohibición de subarrendar"] = st.checkbox(
        "Acepto no subarrendar ni ceder la vivienda sin autorización."
    )
    datos["Acepta uso autorizado"] = st.checkbox(
        "Acepto utilizar el inmueble únicamente para el uso autorizado."
    )
    datos["Quién paga servicios"] = st.radio(
        "Responsabilidad propuesta para el pago de servicios",
        [
            "El inquilino",
            "El propietario",
            "A convenir en el contrato",
        ],
    )
    datos["Requiere condición especial"] = st.text_area(
        "¿Requiere alguna condición o adecuación especial?"
    )
    datos["Observaciones"] = st.text_area("Observaciones adicionales")


def _seccion_privacidad(datos: dict[str, Any]) -> None:
    st.subheader("7. Declaraciones y consentimiento")

    st.info(
        "Los datos se utilizarán únicamente para evaluar esta solicitud, "
        "verificar referencias y contactar al oferente. Si no se formaliza "
        "el alquiler, se eliminarán en un plazo máximo de 90 días, salvo "
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

    if datos["Mayor de edad"] != "Sí":
        st.error("La persona responsable del contrato debe ser mayor de edad.")
        return

    if not validar_correo(datos["Correo electrónico"]):
        st.error("Ingrese una dirección de correo electrónico válida.")
        return

    consentimientos = [
        datos["Declaración de veracidad"],
        datos["Autorización de verificación"],
        datos["Consentimiento de datos"],
    ]
    if not all(consentimientos):
        st.error("Debe aceptar las tres declaraciones finales.")
        return

    condiciones = [
        datos["Acepta monto de alquiler"],
        datos["Acepta depósito"],
        datos["Acepta primer mes adelantado"],
        datos["Acepta contrato escrito"],
        datos["Acepta normas de convivencia"],
        datos["Acepta prohibición de subarrendar"],
        datos["Acepta uso autorizado"],
    ]
    if not all(condiciones):
        st.error("Debe aceptar todas las condiciones de contratación.")
        return

    datos["Número de solicitud"] = generar_numero_solicitud()
    datos["Fecha de envío"] = fecha_hora_costa_rica()

    try:
        guardar_solicitud(
            datos,
            CONFIG.hoja_calculo,
            CONFIG.hoja_respuestas,
        )
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
