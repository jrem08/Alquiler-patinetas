"""Logica de negocio para puntos de acopio."""

from typing import Any

import mysql.connector
from fastapi import HTTPException

from database import get_connection


def _read(query: str, params: tuple[Any, ...] = (), *, many: bool = False) -> Any:
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall() if many else cursor.fetchone()
    except mysql.connector.Error as error:
        raise HTTPException(status_code=503, detail="No fue posible consultar MySQL.") from error
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def _write(query: str, params: tuple[Any, ...] = ()) -> tuple[int, int]:
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        return cursor.lastrowid, cursor.rowcount
    except mysql.connector.IntegrityError as error:
        if connection and connection.is_connected():
            connection.rollback()
        raise HTTPException(status_code=409, detail="La operacion viola una relacion de la base de datos.") from error
    except mysql.connector.Error as error:
        if connection and connection.is_connected():
            connection.rollback()
        raise HTTPException(status_code=503, detail="No fue posible guardar en MySQL.") from error
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def _get_point(point_id: int) -> dict[str, Any]:
    point = _read(
        "SELECT id_punto_acopio, id_zona, nombre, direccion, latitud, longitud, capacidad_maxima "
        "FROM puntos_acopio WHERE id_punto_acopio = %s",
        (point_id,),
    )
    if point is None:
        raise HTTPException(status_code=404, detail="Punto de acopio no encontrado.")
    return point


def _ensure_zone(zone_id: int) -> None:
    if _read("SELECT id_zona FROM zonas WHERE id_zona = %s", (zone_id,)) is None:
        raise HTTPException(status_code=422, detail="El id_zona indicado no existe.")


def list_points(zone_id: int | None = None) -> list[dict[str, Any]]:
    query = (
        "SELECT id_punto_acopio, id_zona, nombre, direccion, latitud, longitud, capacidad_maxima "
        "FROM puntos_acopio"
    )
    if zone_id is not None:
        return _read(query + " WHERE id_zona = %s ORDER BY id_punto_acopio", (zone_id,), many=True)
    return _read(query + " ORDER BY id_punto_acopio", many=True)


def get_point(point_id: int) -> dict[str, Any]:
    return _get_point(point_id)


def create_point(data: dict[str, Any]) -> dict[str, Any]:
    _ensure_zone(data["id_zona"])
    point_id, _ = _write(
        "INSERT INTO puntos_acopio (id_zona, nombre, direccion, latitud, longitud, capacidad_maxima) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            data["id_zona"],
            data["nombre"],
            data["direccion"],
            data["latitud"],
            data["longitud"],
            data["capacidad_maxima"],
        ),
    )
    return _get_point(point_id)


def update_point(point_id: int, data: dict[str, Any], *, partial: bool = False) -> dict[str, Any]:
    _get_point(point_id)
    if "id_zona" in data:
        _ensure_zone(data["id_zona"])

    columns = {
        "id_zona": "id_zona",
        "nombre": "nombre",
        "direccion": "direccion",
        "latitud": "latitud",
        "longitud": "longitud",
        "capacidad_maxima": "capacidad_maxima",
    }
    updates = {columns[key]: value for key, value in data.items()}
    if not updates:
        raise HTTPException(status_code=422, detail="Debe enviar al menos un campo para actualizar.")
    if partial and any(value is None for value in updates.values()):
        raise HTTPException(status_code=422, detail="Los campos no pueden ser null.")

    assignments = ", ".join(f"{column} = %s" for column in updates)
    _write(
        f"UPDATE puntos_acopio SET {assignments} WHERE id_punto_acopio = %s",
        (*updates.values(), point_id),
    )
    return _get_point(point_id)


def delete_point(point_id: int) -> None:
    _get_point(point_id)
    _write("DELETE FROM puntos_acopio WHERE id_punto_acopio = %s", (point_id,))