from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

# Storage en memoria para el prototipo (en producción: PostgreSQL)
alarms_db: dict = {}


class AlarmCreate(BaseModel):
    user_id: str
    medication_name: str
    dose: str
    times: list[str]  # Ej: ["08:00", "14:00", "20:00"]
    days_of_week: Optional[list[int]] = [0, 1, 2, 3, 4, 5, 6]
    caregiver_email: Optional[str] = None
    caregiver_phone: Optional[str] = None


class AlarmConfirm(BaseModel):
    alarm_id: str
    confirmed_at: Optional[str] = None


@router.post("/alarmas")
async def crear_alarma(alarm: AlarmCreate):
    """
    RF03/RF04: Configura recordatorio de toma de medicamento.
    La alarma ejecuta localmente en el dispositivo (IndexedDB / Service Worker).
    """
    alarm_id = f"alarm_{alarm.user_id}_{len(alarms_db) + 1}"

    alarms_db[alarm_id] = {
        "id": alarm_id,
        "user_id": alarm.user_id,
        "medication_name": alarm.medication_name,
        "dose": alarm.dose,
        "times": alarm.times,
        "days_of_week": alarm.days_of_week,
        "caregiver_email": alarm.caregiver_email,
        "caregiver_phone": alarm.caregiver_phone,
        "active": True,
        "created_at": datetime.now().isoformat(),
        "confirmations": [],
    }

    return {
        "alarm_id": alarm_id,
        "message": f"Alarma creada para {alarm.medication_name}",
        "times": alarm.times,
    }


@router.get("/alarmas/{user_id}")
async def listar_alarmas(user_id: str):
    """Retorna todas las alarmas de un usuario."""
    user_alarms = [a for a in alarms_db.values() if a["user_id"] == user_id and a["active"]]
    return {"user_id": user_id, "alarms": user_alarms}


@router.post("/alarmas/confirmar")
async def confirmar_toma(confirm: AlarmConfirm):
    """
    RF04: Registra la confirmación explícita de toma del medicamento.
    Actualiza el historial y cancela alerta al cuidador si pendiente.
    """
    if confirm.alarm_id not in alarms_db:
        raise HTTPException(status_code=404, detail="Alarma no encontrada")

    alarm = alarms_db[confirm.alarm_id]
    confirmation = {
        "confirmed_at": confirm.confirmed_at or datetime.now().isoformat(),
        "recorded_at": datetime.now().isoformat(),
    }
    alarm["confirmations"].append(confirmation)

    return {
        "alarm_id": confirm.alarm_id,
        "medication": alarm["medication_name"],
        "status": "confirmed",
        "message": "Toma registrada correctamente",
    }


@router.delete("/alarmas/{alarm_id}")
async def eliminar_alarma(alarm_id: str):
    """Desactiva una alarma."""
    if alarm_id not in alarms_db:
        raise HTTPException(status_code=404, detail="Alarma no encontrada")

    alarms_db[alarm_id]["active"] = False
    return {"message": "Alarma eliminada"}
