"""API REST del requisito PAT-0003: CRUD de puntos de acopio por zona."""

from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query, Response
from pydantic import BaseModel, ConfigDict, Field

import services

app = FastAPI(
    title="API de Alquiler de Patinetas",
    description="Gestion de puntos de acopio asociados a zonas existentes (PAT-0003).",
    version="1.0.0",
)


class PointInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_zona: int = Field(gt=0, description="Identificador de una zona existente.")
    nombre: str = Field(min_length=2, max_length=100)
    direccion: str = Field(min_length=3, max_length=200)
    latitud: float = Field(ge=-90, le=90)
    longitud: float = Field(ge=-180, le=180)
    capacidad_maxima: int = Field(gt=0)


class PointPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id_zona: int | None = Field(default=None, gt=0)
    nombre: str | None = Field(default=None, min_length=2, max_length=100)
    direccion: str | None = Field(default=None, min_length=3, max_length=200)
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)
    capacidad_maxima: int | None = Field(default=None, gt=0)


PointId = Annotated[int, Path(gt=0, description="ID del punto de acopio")]


@app.get("/puntos-acopio", tags=["Puntos de acopio"])
def list_points(id_zona: Annotated[int | None, Query(gt=0)] = None):
    """Lista los puntos de acopio; permite filtrar por zona."""
    return services.list_points(id_zona)


@app.get("/puntos-acopio/{point_id}", tags=["Puntos de acopio"])
def get_point(point_id: PointId):
    """Consulta un punto de acopio por su ID."""
    return services.get_point(point_id)


@app.post("/puntos-acopio", status_code=201, tags=["Puntos de acopio"])
def create_point(data: PointInput):
    """Crea un punto y comprueba que la zona exista."""
    return services.create_point(data.model_dump())


@app.put("/puntos-acopio/{point_id}", tags=["Puntos de acopio"])
def replace_point(point_id: PointId, data: PointInput):
    """Reemplaza todos los campos editables de un punto."""
    return services.update_point(point_id, data.model_dump())


@app.patch("/puntos-acopio/{point_id}", tags=["Puntos de acopio"])
def patch_point(point_id: PointId, data: PointPatch):
    """Actualiza solo los campos enviados."""
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=422, detail="Debe enviar al menos un campo para actualizar.")
    return services.update_point(point_id, updates, partial=True)


@app.delete("/puntos-acopio/{point_id}", status_code=204, tags=["Puntos de acopio"])
def delete_point(point_id: PointId) -> Response:
    """Elimina un punto de acopio."""
    services.delete_point(point_id)
    return Response(status_code=204)