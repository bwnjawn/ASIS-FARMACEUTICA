from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class MissedDoseAlert(BaseModel):
    user_id: str
    alarm_id: str
    medication_name: str
    scheduled_time: str
    caregiver_email: Optional[str] = None
    caregiver_phone: Optional[str] = None


async def send_caregiver_email(
    caregiver_email: str, patient_name: str, medication: str, time: str
):
    """
    Envía alerta por email al cuidador.
    En producción: integración con SendGrid/Mailgun.
    """
    logger.info(
        f"[EMAIL] Alerta a {caregiver_email}: "
        f"{patient_name} no confirmó {medication} a las {time}"
    )
    # TODO: Integrar proveedor SMTP (SendGrid, Mailgun)


async def send_caregiver_sms(
    phone: str, patient_name: str, medication: str, time: str
):
    """
    Envía alerta SMS al cuidador.
    En producción: integración con Twilio.
    """
    logger.info(
        f"[SMS] Alerta a {phone}: "
        f"{patient_name} no confirmó {medication} a las {time}"
    )
    # TODO: Integrar Twilio


@router.post("/notificaciones/alerta-cuidador")
async def alertar_cuidador(alert: MissedDoseAlert, background_tasks: BackgroundTasks):
    """
    Notifica al cuidador/familiar cuando el usuario no confirma
    la toma del medicamento en 15 minutos.
    Esta ruta es invocada por el Service Worker de la PWA.
    """
    notifications_sent = []

    if alert.caregiver_email:
        background_tasks.add_task(
            send_caregiver_email,
            alert.caregiver_email,
            f"Usuario {alert.user_id}",
            alert.medication_name,
            alert.scheduled_time,
        )
        notifications_sent.append("email")

    if alert.caregiver_phone:
        background_tasks.add_task(
            send_caregiver_sms,
            alert.caregiver_phone,
            f"Usuario {alert.user_id}",
            alert.medication_name,
            alert.scheduled_time,
        )
        notifications_sent.append("sms")

    if not notifications_sent:
        raise HTTPException(
            status_code=400,
            detail="No hay datos de contacto del cuidador registrados",
        )

    return {
        "status": "sent",
        "notifications": notifications_sent,
        "message": f"Cuidador notificado sobre {alert.medication_name} a las {alert.scheduled_time}",
    }
