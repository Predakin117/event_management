# event_management

Aplicación web en **Django + SQLite** para administrar eventos, registrar invitados y permitir que los asistentes consulten su invitación escribiendo su número de cédula. No usa JavaScript ni librerías externas.

## Estructura (feature-driven)

| App | Responsabilidad |
|---|---|
| `config` | Configuración global y enrutador principal de URLs |
| `core` | Plantilla base (`base.html`) y CSS global. Sin modelos |
| `eventos` | Modelo `Evento` y vistas públicas (lista y detalle) |
| `invitados` | Modelo `Invitado` (cédula + clave foránea a `Evento`). Solo desde el admin |
| `confirmacion` | `FormularioCedula`, `servicios.buscar_invitaciones(cedula)` y `confirmar.html`. Sin modelos |

Las dependencias van en una sola dirección: `confirmacion → invitados → eventos`. Ninguna app depende de `core` en Python.

## Flujo de una petición

`urls.py` → `views.py` → `models.py` → contexto → template (+ CSS) → HTML.

## Cómo ejecutarlo (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Sitio público: http://127.0.0.1:8000/
- Confirmar invitación: http://127.0.0.1:8000/confirmacion/
- Panel de administración: http://127.0.0.1:8000/admin/ (crea eventos e invitados aquí)

## Pruebas

```powershell
python manage.py test
```
# event_management
# event_management
