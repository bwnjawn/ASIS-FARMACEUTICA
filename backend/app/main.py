import asyncio
import os
import sys

# BLINDAJE PARA WINDOWS: Debe estar en la línea 1, antes de importar FastAPI o Playwright
if sys.platform == "win32":
    # Forzamos a Windows a usar el motor que soporta subprocesos de Chromium
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.services.yapp_scraper import renovar_token_yapp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # Leemos en qué entorno estamos
    env = os.getenv("ENVIRONMENT", "production")

    if env == "development":
        logger.info(
            "🛠️ MODO DESARROLLO: Saltando el bot de YAPP. El servidor iniciará al instante para usar --reload."
        )
    else:
        logger.info(
            "🚀 MODO PRODUCCIÓN: Iniciando bot de Playwright para obtener token de YAPP..."
        )
        try:
            await renovar_token_yapp()
        except Exception as e:
            logger.error(f"Fallo al iniciar el bot de YAPP: {e}")

        scheduler.add_job(renovar_token_yapp, "interval", minutes=120)
        scheduler.start()

    yield

    if env != "development":
        scheduler.shutdown()


app = FastAPI(title="ASIS Farmacéutica API MVC", lifespan=lifespan)

# Permitir que el frontend (Vue/Quasar) se conecte sin errores de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"mensaje": "API de ASIS Farmacéutica operando bajo patrón MVC"}


from app.services.supabase_client import supabase


@app.get("/test-supabase")
async def test_supabase():
    try:
        # Intentamos hacer una consulta simple a la tabla paciente
        respuesta = supabase.table("paciente").select("*").execute()
        return {
            "status": "Conexión Exitosa con Supabase",
            "datos_encontrados": respuesta.data,
        }
    except Exception as e:
        return {"status": "Error de conexión", "detalle": str(e)}
