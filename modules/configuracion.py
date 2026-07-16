from dataclasses import dataclass


@dataclass(frozen=True)
class ConfiguracionInmueble:
    titulo: str = "Casa en alquiler — Higuito Centro"
    ubicacion: str = "Higuito Centro, frente al Palí"
    alquiler_habitacional: str = "₡380 000 mensuales"
    deposito: str = "₡380 000"
    contacto: str = "admin@vigias.net"
    telefono: str = "8715-5477"
    hoja_calculo: str = "Respuestas_Alquiler"
    hoja_respuestas: str = "Formulario_Completo"
    imagen_fachada: str = "assets/fachada1.jpg"
    imagen_caracteristicas: str = "assets/Carac.jpg"
    video_url: str = "https://youtu.be/9U7l9rvnVJc"
    mapa_url: str = (
        "https://www.google.com/maps/embed?pb="
        "!1m14!1m12!1m3!1d245.67975692153937!"
        "2d-84.05487347043625!3d9.86076000110528!"
        "2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!"
        "5e0!3m2!1ses-419!2scr!4v1752880163707!"
        "5m2!1ses-419!2scr"
    )


CONFIG = ConfiguracionInmueble()
