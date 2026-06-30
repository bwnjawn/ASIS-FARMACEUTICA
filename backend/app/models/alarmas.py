from datetime import datetime, time
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AlarmaBase(BaseModel):
    nombre_medicamento: str = Field(..., description="Nombre del remedio a tomar")
    dosis: str = Field(..., description="Ej: '1 comprimido' o '15 ml'")
    hora_programada: time = Field(
        ..., description="Hora de la primera toma, ej: '08:00:00'"
    )
    activo: bool = Field(
        default=True, description="True si el recordatorio está activo"
    )


class AlarmaCreate(AlarmaBase):
    id_paciente: UUID = Field(..., description="UUID del paciente en Supabase")


# --- NUEVO MODELO PARA ACTUALIZACIONES ---
class AlarmaUpdate(BaseModel):
    nombre_medicamento: Optional[str] = Field(
        None, description="Nuevo nombre del remedio"
    )
    dosis: Optional[str] = Field(None, description="Nueva dosis")
    hora_programada: Optional[time] = Field(None, description="Nueva hora de la toma")
    activo: Optional[bool] = Field(
        None, description="Cambiar estado activo/inactivo (True/False)"
    )


class AlarmaResponse(AlarmaBase):
    id_recordatorio: int
    id_paciente: UUID
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
