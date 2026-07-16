import re
from typing import Any


PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_correo(correo: str) -> bool:
    return bool(PATRON_CORREO.match(correo.strip()))


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
