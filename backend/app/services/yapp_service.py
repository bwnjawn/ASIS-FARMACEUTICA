"""
Servicio de integración con la API de YAPP.
Maneja búsqueda de medicamentos y cotización de precios.
"""

import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

YAPP_HEADERS = {
    "accept": "*/*",
    "accept-language": "es-ES,es;q=0.9",
    "client-id": "f54834cd-e9b3-11eb-a606-067f",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://web.yapp.cl",
    "referer": "https://web.yapp.cl/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

YAPP_AUTOCOMPLETE_URL = "https://api-integration.yapp.cl/v2/vademecum/autocomplete"
YAPP_QUOTATION_URL = "https://api-integration.yapp.cl/v2/quotation"

# Coordenadas fijas de Puerto Montt
PUERTO_MONTT_LAT = -41.4693
PUERTO_MONTT_LNG = -72.9424
PUERTO_MONTT_COMMUNE_ID = 10101


async def search_medications(text: str, auth_token: str) -> list[dict]:
    """
    Busca medicamentos por nombre o principio activo via YAPP autocomplete.
    RF01: Búsqueda por nombre comercial o principio activo.
    """
    headers = {**YAPP_HEADERS, "authorization": f"Bearer {auth_token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(
                YAPP_AUTOCOMPLETE_URL,
                params={"text": text, "external_vademecum": "0"},
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("data", [])

            # Filtramos solo los que tienen product_id válido
            return [item for item in results if item.get("product_id")]

        except httpx.TimeoutException:
            logger.error("Timeout al conectar con YAPP autocomplete")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP {e.response.status_code} en YAPP autocomplete")
            raise


async def get_quotation(
    product_id: str,
    auth_token: str,
    lat: Optional[float] = None,
    lng: Optional[float] = None,
) -> list[dict]:
    """
    Cotiza un medicamento en farmacias cercanas.
    RF02: Comparación de precios ordenada por geolocalización.
    """
    lat = lat or PUERTO_MONTT_LAT
    lng = lng or PUERTO_MONTT_LNG

    headers = {**YAPP_HEADERS, "authorization": f"Bearer {auth_token}"}

    payload = (
        f'{{"products":[{{"id":"{product_id}","result_id":""}}],'
        f'"coords":{{"lat":{lat},"lng":{lng}}},"commune_id":{PUERTO_MONTT_COMMUNE_ID}}}'
    )

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.post(
                YAPP_QUOTATION_URL,
                data=payload,
                headers=headers,
            )
            response.raise_for_status()
            data = response.json()
            pharmacies = data.get("data", [])

            # Ordenamos: primero con distancia (cercanía), luego por precio
            with_distance = [p for p in pharmacies if p.get("pharmacy_distance") is not None]
            without_distance = [p for p in pharmacies if p.get("pharmacy_distance") is None]

            with_distance.sort(key=lambda x: (x.get("pharmacy_distance", 999), x.get("total", 999)))
            without_distance.sort(key=lambda x: x.get("total", 999))

            return with_distance + without_distance

        except httpx.TimeoutException:
            logger.error("Timeout al conectar con YAPP quotation")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"Error HTTP {e.response.status_code} en YAPP quotation")
            raise
