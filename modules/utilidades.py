from datetime import datetime
from zoneinfo import ZoneInfo
from uuid import uuid4


ZONA_COSTA_RICA = ZoneInfo("America/Costa_Rica")


def fecha_hora_costa_rica() -> str:
    return datetime.now(ZONA_COSTA_RICA).strftime("%Y-%m-%d %H:%M:%S")


def generar_numero_solicitud() -> str:
    fecha = datetime.now(ZONA_COSTA_RICA).strftime("%Y%m%d")
    codigo = uuid4().hex[:8].upper()
    return f"ALQ-{fecha}-{codigo}"
