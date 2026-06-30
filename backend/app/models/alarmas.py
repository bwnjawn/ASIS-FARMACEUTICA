from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, Field


# 1. Modelo Base: Ajustado a los nombres reales de la tabla 'recordatorio'
class AlarmaBase(BaseModel):
    id_producto: str = Field(..., description="ID del medicamento de YAPP")
    nombre_medicamento: str = Field(..., description="Nombre del remedio a tomar")
    dosis: str = Field(..., description="Ej: '1 comprimido' o '15 ml'")
    # Nota: frecuencia_horas no está en tu SQL actual, si la necesitas, déjala aquí.
    # frecuencia_horas: int = Field(..., gt=0, description="Cada cuántas horas, ej: 8")
    hora_programada: time = Field(
        ..., description="Hora de la primera toma, ej: '08:00:00'"
    )
    activo: bool = Field(
        default=True, description="True si el recordatorio está activo"
    )


# 2. Modelo de Creación
class AlarmaCreate(AlarmaBase):
    id_paciente: str = Field(..., description="UUID del paciente en Supabase")


# 3. Modelo de Respuesta
class AlarmaResponse(AlarmaBase):
    id_recordatorio: int  # Cambiado para coincidir con tu PK
    id_paciente: str
    creado_en: Optional[datetime] = None

    class Config:
        from_attributes = True
