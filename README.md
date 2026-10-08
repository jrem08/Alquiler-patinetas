# PAT-0003: CRUD de puntos de acopio

API REST en FastAPI para crear, consultar, editar y eliminar puntos de acopio relacionados con una zona existente. Todas las respuestas de la API son JSON; el endpoint DELETE responde con HTTP 204 sin cuerpo.

## Preparar MySQL con Workbench

1. Inicia tu servidor MySQL y abre una conexion en MySQL Workbench. Workbench es el cliente para ejecutar los scripts; el servidor MySQL debe estar instalado y activo.
2. Abre y ejecuta `sql/01_create_database.sql` con una cuenta administradora. Crea las tablas `zonas` y `puntos_acopio`, la relacion FK y una zona inicial de prueba.
3. En Workbench abre `sql/02_create_user.sql` y cambia `CAMBIA_ESTA_CLAVE` por una clave propia. Ejecuta el script con permisos de administracion.
4. Copia `.env.example` como `.env` y usa la misma clave asignada al usuario `alquiler_api`. Si tu servidor no es local, ajusta `DB_HOST`.

## Instalar y ejecutar

En PowerShell, desde la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
uvicorn main:app --reload
```

Documentacion interactiva y prueba de endpoints: `http://127.0.0.1:8000/docs`.

## Endpoints

| Metodo | Ruta | Funcion |
| --- | --- | --- |
| GET | `/puntos-acopio` | Lista todos; acepta `?id_zona=1` |
| GET | `/puntos-acopio/{point_id}` | Consulta un punto |
| POST | `/puntos-acopio` | Crea un punto y verifica `id_zona` |
| PUT | `/puntos-acopio/{point_id}` | Reemplaza todos los campos |
| PATCH | `/puntos-acopio/{point_id}` | Actualiza solo los campos enviados |
| DELETE | `/puntos-acopio/{point_id}` | Elimina un punto |

Ejemplo de JSON para POST y PUT:

```json
{
  "id_zona": 1,
  "nombre": "Acopio Centro",
  "direccion": "Carrera 10 # 20-30",
  "latitud": 4.60971,
  "longitud": -74.08175,
  "capacidad_maxima": 25
}
```

La API valida rangos de coordenadas, capacidad, campos extra y existencia de la zona. Los errores se entregan como JSON con un codigo HTTP apropiado.