# Alquiler Higuito V2

Aplicación Streamlit para presentar una casa en alquiler y recopilar
información de posibles inquilinos.

## Estructura

```text
alquiler_higuito_v2/
├── app.py
├── assets/
│   ├── fachada1.jpg
│   └── Carac.jpg
├── modules/
│   ├── configuracion.py
│   ├── correo.py
│   ├── formulario.py
│   ├── google_sheets.py
│   ├── inmueble.py
│   ├── utilidades.py
│   └── validaciones.py
├── .streamlit/
│   ├── config.toml
│   └── secrets.example.toml
├── requirements.txt
└── .gitignore
```

## Preparación

1. Copie sus imágenes a `assets/fachada1.jpg` y `assets/Carac.jpg`.
2. Cree en Google Sheets el archivo `Respuestas_Alquiler`.
3. Cree una pestaña llamada `Formulario_Completo`.
4. Comparta la hoja con el correo de la cuenta de servicio.
5. En local, copie:

```bash
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

6. Complete las credenciales reales en `secrets.toml`.
7. Instale las dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

8. Ejecute:

```bash
streamlit run app.py
```

## Streamlit Community Cloud

Pegue el contenido de su `secrets.toml` en:

```text
Manage app → Settings → Secrets
```

No suba `secrets.toml` ni credenciales JSON a GitHub.
