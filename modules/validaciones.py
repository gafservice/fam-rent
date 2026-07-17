import re
from typing import Any


PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_correo(correo: str) -> bool:
    return bool(PATRON_CORREO.match(correo.strip()))


def normalizar_telefono(telefono: str) -> str:
    """Devuelve un teléfono de Costa Rica en formato 8888-8888."""
    digitos = re.sub(r"\D", "", telefono)

    if len(digitos) == 11 and digitos.startswith("506"):
        digitos = digitos[3:]

    if len(digitos) != 8:
        return telefono.strip()

    return f"{digitos[:4]}-{digitos[4:]}"


def validar_telefono(telefono: str) -> bool:
    """Acepta ocho dígitos, con separadores y prefijo +506 opcional."""
    digitos = re.sub(r"\D", "", telefono)

    if len(digitos) == 11 and digitos.startswith("506"):
        digitos = digitos[3:]

    return len(digitos) == 8


def campos_obligatorios_faltantes(
    datos: dict[str, Any],
    campos: list[str],
) -> list[str]:
    faltantes: list[str] = []

    for campo in campos:
        valor = datos.get(campo)

        if valor is None:
            faltantes.append(campo)
        elif isinstance(valor, str) and not valor.strip():
            faltantes.append(campo)

    return faltantes

