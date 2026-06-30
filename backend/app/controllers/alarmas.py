from typing import List

from app.models.alarmas import AlarmaCreate, AlarmaResponse
from app.services.supabase_client import supabase
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/alarmas", tags=["Alarmas y Recordatorios"])


@router.post("/", response_model=AlarmaResponse)
async def crear_alarma(alarma: AlarmaCreate):
    try:
        datos_insertar = alarma.model_dump()

        # Mapeo de campos de tu modelo a las columnas de la tabla 'recordatorio'
        # Ajustamos los nombres para que coincidan con tu nuevo SQL
        payload = {
            "id_paciente": datos_insertar["id_paciente"],
            "nombre_medicamento": datos_insertar["nombre_medicamento"],
            "dosis": datos_insertar["dosis"],
            "hora_programada": datos_insertar["hora_inicio"].strftime("%H:%M:%S"),
            "activo": datos_insertar["estado"],
        }

        # Cambiamos 'alarma' por 'recordatorio'
        respuesta = supabase.table("recordatorio").insert(payload).execute()

        if not respuesta.data:
            raise HTTPException(
                status_code=400, detail="No se pudo guardar el recordatorio"
            )

        return respuesta.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id_paciente}", response_model=List[AlarmaResponse])
async def obtener_alarmas(id_paciente: str):
    """
    Devuelve todas las alarmas activas de un paciente en específico.
    """
    try:
        respuesta = (
            supabase.table("alarma")
            .select("*")
            .eq("id_paciente", id_paciente)
            .execute()
        )
        return respuesta.data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
