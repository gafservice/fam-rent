from typing import Any

import gspread
import streamlit as st


COLUMNAS = [
    "Número de solicitud",
    "Fecha de envío",
    "Tipo de uso",
    "Nombre completo",
    "Identificación",
    "Mayor de edad",
    "Teléfono principal",
    "Teléfono alternativo",
    "Correo electrónico",
    "Medio preferido de contacto",
    "Profesión u ocupación",
    "Empresa o actividad",
    "Puesto",
    "Antigüedad laboral",
    "Ingreso mensual aproximado",
    "Otros ingresos",
    "Comprobante de ingresos",
    "Fecha prevista de ingreso",
    "Plazo previsto de alquiler",
    "Cantidad de ocupantes",
    "Adultos",
    "Menores y edades",
    "Relación entre ocupantes",
    "Trabajo desde la vivienda",
    "Mascotas",
    "Detalle de mascotas",
    "Tenencia responsable",
    "Cantidad de vehículos",
    "Necesita parqueo adicional",
    "Actualmente alquila",
    "Zona del alquiler anterior",
    "Tiempo en alquiler anterior",
    "Motivo de salida",
    "Propietario anterior",
    "Contacto propietario anterior",
    "Autoriza contactar referencia",
    "Referencia laboral",
    "Teléfono referencia laboral",
    "Referencia personal",
    "Teléfono referencia personal",
    "Acepta monto de alquiler",
    "Acepta depósito",
    "Acepta primer mes adelantado",
    "Acepta contrato escrito",
    "Acepta normas de convivencia",
    "Acepta prohibición de subarrendar",
    "Acepta uso autorizado",
    "Quién paga servicios",
    "Requiere condición especial",
    "Observaciones",
    "Declaración de veracidad",
    "Autorización de verificación",
    "Consentimiento de datos",
]


def _cliente_gspread() -> gspread.Client:
    credenciales = dict(st.secrets["gcp_service_account"])
    return gspread.service_account_from_dict(credenciales)


def guardar_solicitud(
    datos: dict[str, Any],
    nombre_archivo: str,
    nombre_hoja: str,
) -> None:
    cliente = _cliente_gspread()
    hoja = cliente.open(nombre_archivo).worksheet(nombre_hoja)

    if not hoja.row_values(1):
        hoja.append_row(COLUMNAS, value_input_option="USER_ENTERED")

    fila = [str(datos.get(columna, "")) for columna in COLUMNAS]
    hoja.append_row(fila, value_input_option="USER_ENTERED")
