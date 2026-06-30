from datetime import datetime
from typing import List
from uuid import UUID

# Asegúrate de importar AlarmaUpdate desde tus modelos
from app.models.alarmas import AlarmaCreate, AlarmaResponse, AlarmaUpdate
from app.services.supabase_client import supabase
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/alarmas", tags=["Alarmas y Recordatorios"])


@router.post("/", response_model=AlarmaResponse)
async def crear_alarma(alarma: AlarmaCreate):
    try:
        datos_insertar = alarma.model_dump()
        payload = {
            "id_paciente": str(datos_insertar["id_paciente"]),
            "nombre_medicamento": datos_insertar["nombre_medicamento"],
            "dosis": datos_insertar["dosis"],
            "hora_programada": datos_insertar["hora_programada"].strftime("%H:%M:%S"),
            "activo": datos_insertar["activo"],
        }
        respuesta = supabase.table("recordatorio").insert(payload).execute()
        if not respuesta.data:
            raise HTTPException(
                status_code=400, detail="No se pudo guardar el recordatorio"
            )
        return respuesta.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id_paciente}", response_model=List[AlarmaResponse])
async def obtener_alarmas(id_paciente: UUID):
    try:
        respuesta = (
            supabase.table("recordatorio")
            .select("*")
            .eq("id_paciente", str(id_paciente))
            .execute()
        )
        return respuesta.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================================================================
# NUEVOS ENDPOINTS: ACTUALIZAR (DESACTIVAR) Y ELIMINAR
# ==============================================================================


@router.patch("/{id_recordatorio}", response_model=AlarmaResponse)
async def actualizar_alarma(id_recordatorio: int, alarma_update: AlarmaUpdate):
    """
    Permite actualizar parcialmente una alarma.
    Ideal para activar/desactivar (enviar {"activo": false}) o editar detalles.
    """
    try:
        # Extraemos solo los campos que el cliente envió en el JSON
        datos_recibidos = alarma_update.model_dump(exclude_none=True)

        if not datos_recibidos:
            raise HTTPException(
                status_code=400, detail="No se enviaron campos para modificar"
            )

        # Si cambiaron la hora, la formateamos adecuadamente para PostgreSQL (TIME)
        if "hora_programada" in datos_recibidos:
            datos_recibidos["hora_programada"] = datos_recibidos[
                "hora_programada"
            ].strftime("%H:%M:%S")

        # Ejecutamos la actualización en la tabla 'recordatorio' usando la PK id_recordatorio
        respuesta = (
            supabase.table("recordatorio")
            .update(datos_recibidos)
            .eq("id_recordatorio", id_recordatorio)
            .execute()
        )

        if not respuesta.data:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el recordatorio con ID {id_recordatorio}",
            )

        return respuesta.data[0]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{id_recordatorio}")
async def eliminar_alarma(id_recordatorio: int):
    """
    Elimina físicamente un recordatorio de la base de datos por su ID.
    """
    try:
        respuesta = (
            supabase.table("recordatorio")
            .delete()
            .eq("id_recordatorio", id_recordatorio)
            .execute()
        )

        if not respuesta.data:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el recordatorio con ID {id_recordatorio}",
            )

        return {
            "status": "success",
            "mensaje": f"Recordatorio {id_recordatorio} eliminado correctamente",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TomaRemedio(BaseModel):
    estado: str
    fecha_hora_real: datetime


# Agrega este endpoint al final de alarmas.py
@router.post("/{id_recordatorio}/tomar")
async def registrar_toma(id_recordatorio: int, toma: TomaRemedio):
    try:
        # Insertamos en la tabla 'historial_toma' que creamos en el SQL
        payload = {
            "id_recordatorio": id_recordatorio,
            "fecha_hora_real": toma.fecha_hora_real.isoformat(),
            "estado": toma.estado,
        }

        respuesta = supabase.table("historial_toma").insert(payload).execute()

        if not respuesta.data:
            raise HTTPException(status_code=400, detail="Error al guardar en Supabase")

        return {"status": "success", "data": respuesta.data[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
