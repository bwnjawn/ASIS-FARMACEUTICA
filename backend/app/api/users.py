from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import secrets

router = APIRouter()

# Storage en memoria para el prototipo
users_db: dict = {}
caregiver_codes: dict = {}


class UserCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None


class CaregiverLink(BaseModel):
    user_id: str
    code: str


@router.post("/usuarios")
async def crear_usuario(user: UserCreate):
    """Registra un nuevo usuario en el sistema."""
    user_id = f"user_{len(users_db) + 1}"
    users_db[user_id] = {
        "id": user_id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "caregiver_id": None,
        "medical_history": [],
    }
    return {"user_id": user_id, "name": user.name}


@router.get("/usuarios/{user_id}")
async def obtener_usuario(user_id: str):
    """Obtiene datos del usuario."""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return users_db[user_id]


@router.post("/usuarios/{user_id}/codigo-cuidador")
async def generar_codigo_cuidador(user_id: str):
    """
    RF06: Genera código de vinculación para que un cuidador pueda
    supervisar remotamente las tomas del usuario.
    """
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    code = secrets.token_hex(3).upper()  # Código de 6 caracteres (ej: "A3F9C2")
    caregiver_codes[code] = user_id

    return {
        "user_id": user_id,
        "code": code,
        "message": "Entrega este código a tu cuidador o familiar",
        "instructions": "El cuidador debe ingresar este código en su aplicación para vincularse",
    }


@router.post("/cuidadores/vincular")
async def vincular_cuidador(link: CaregiverLink):
    """
    RF06: Vincula un cuidador a un usuario mediante el código generado.
    """
    if link.code not in caregiver_codes:
        raise HTTPException(status_code=400, detail="Código inválido o expirado")

    patient_id = caregiver_codes[link.code]
    if patient_id not in users_db:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    users_db[patient_id]["caregiver_id"] = link.user_id
    del caregiver_codes[link.code]

    return {
        "message": "Vinculación exitosa",
        "patient": users_db[patient_id]["name"],
        "caregiver_id": link.user_id,
    }
