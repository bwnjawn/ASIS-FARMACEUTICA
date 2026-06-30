import random
import string

from app.models.auth import AuthLogin, RegistroPaciente
from app.services.supabase_client import supabase
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


def generar_email_rut(rut: str) -> str:
    """Convierte un RUT en un email ficticio para Supabase Auth"""
    rut_limpio = rut.replace(".", "").strip()
    return f"{rut_limpio}@asis.cl"


def generar_codigo_vinculacion() -> str:
    """Genera un código aleatorio de 6 caracteres (letras mayúsculas y números)"""
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


@router.post("/registro/paciente")
async def registrar_paciente(datos: RegistroPaciente):
    email_auth = generar_email_rut(datos.rut)

    try:
        # 1. Crear el usuario en la bóveda de seguridad de Supabase (auth.users)
        auth_response = supabase.auth.sign_up(
            {"email": email_auth, "password": datos.password}
        )

        if not auth_response.user:
            raise HTTPException(
                status_code=400, detail="Error al crear el usuario en Supabase Auth"
            )

        nuevo_id = auth_response.user.id
        codigo_vinculo = generar_codigo_vinculacion()

        # 2. Guardar el perfil público en la tabla 'paciente'
        payload_paciente = {
            "id_paciente": nuevo_id,
            "nombre_usuario": datos.nombre_usuario,
            "rut": datos.rut,
            "codigo_vinculacion": codigo_vinculo,
        }

        db_response = supabase.table("paciente").insert(payload_paciente).execute()

        if not db_response.data:
            raise HTTPException(
                status_code=400, detail="Error al guardar el perfil del paciente"
            )

        return {
            "mensaje": "Paciente registrado exitosamente",
            "id_paciente": nuevo_id,
            "codigo_vinculacion": codigo_vinculo,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def iniciar_sesion(credenciales: AuthLogin):
    email_auth = generar_email_rut(credenciales.rut)

    try:
        # Iniciar sesión contra Supabase
        auth_response = supabase.auth.sign_in_with_password(
            {"email": email_auth, "password": credenciales.password}
        )

        if not auth_response.session:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        return {
            "mensaje": "Inicio de sesión exitoso",
            "access_token": auth_response.session.access_token,
            "id_usuario": auth_response.user.id,
        }

    except Exception:
        raise HTTPException(status_code=401, detail="RUT o contraseña incorrectos")
