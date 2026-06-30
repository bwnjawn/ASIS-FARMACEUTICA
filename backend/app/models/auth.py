from pydantic import BaseModel, Field


class AuthLogin(BaseModel):
    rut: str = Field(
        ..., description="RUT del usuario sin puntos y con guion, ej: 12345678-9"
    )
    password: str = Field(..., description="Contraseña o PIN del usuario")


class RegistroPaciente(BaseModel):
    rut: str = Field(..., description="RUT del paciente")
    nombre_usuario: str = Field(..., description="Nombre completo o alias")
    password: str = Field(..., description="Contraseña para la cuenta")
