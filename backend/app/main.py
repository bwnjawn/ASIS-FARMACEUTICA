from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import medications, alarms, users, notifications

app = FastAPI(
    title="ASIS Farmacéutica API",
    description="Sistema de asistencia farmacéutica para adultos mayores - Puerto Montt",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(medications.router, prefix="/api/v1", tags=["Medicamentos"])
app.include_router(alarms.router, prefix="/api/v1", tags=["Alarmas"])
app.include_router(users.router, prefix="/api/v1", tags=["Usuarios"])
app.include_router(notifications.router, prefix="/api/v1", tags=["Notificaciones"])


@app.get("/")
async def root():
    return {
        "message": "ASIS Farmacéutica API activa",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
