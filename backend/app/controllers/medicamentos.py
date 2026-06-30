import httpx
from app.services.yapp_scraper import obtener_token_actual
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/medicamentos", tags=["Medicamentos (YAPP)"])

# Cabeceras estándar requeridas por la seguridad de YAPP
YAPP_HEADERS = {
    "accept": "*/*",
    "accept-language": "es-ES,es;q=0.9",
    "client-id": "f54834cd-e9b3-11eb-a606-067f",
    "content-type": "text/plain;charset=UTF-8",
    "origin": "https://web.yapp.cl",
    "referer": "https://web.yapp.cl/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}


@router.get("/buscar")
async def buscar_medicamento(
    q: str = Query(..., description="Nombre del medicamento a buscar"),
):
    """
    Endpoint para el buscador de texto libre (Autocompletado).
    RF01: Búsqueda por nombre comercial o principio activo.
    """
    token = obtener_token_actual()
    if not token:
        raise HTTPException(
            status_code=503,
            detail="El token de YAPP aún no está listo. Intente en unos segundos.",
        )

    # URL correcta de la API de integración
    url = "https://api-integration.yapp.cl/v2/vademecum/autocomplete"
    params = {"text": q, "external_vademecum": "0"}

    headers = {**YAPP_HEADERS, "authorization": f"Bearer {token}"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url, params=params, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error en YAPP: {response.text}",
            )

        try:
            data = response.json()
            resultados = data.get("data", [])
            # Filtramos para devolver solo los que tienen un ID de producto válido (como en tu prototipo)
            productos_validos = [item for item in resultados if item.get("product_id")]
            return {"data": productos_validos}
        except Exception:
            raise HTTPException(
                status_code=500, detail="Error decodificando la respuesta de YAPP"
            )


@router.get("/cotizar")
async def cotizar_medicamento(
    id_producto: str = Query(..., description="ID del producto de YAPP (ej. '12345')"),
    lat: float = Query(-41.4693, description="Latitud (Por defecto Puerto Montt)"),
    lng: float = Query(-72.9424, description="Longitud (Por defecto Puerto Montt)"),
):
    """
    Endpoint para cotizar un medicamento específico.
    RF02: Comparación de precios ordenada por geolocalización.
    """
    token = obtener_token_actual()
    if not token:
        raise HTTPException(status_code=503, detail="Token no disponible")

    url = "https://api-integration.yapp.cl/v2/quotation"
    headers = {**YAPP_HEADERS, "authorization": f"Bearer {token}"}

    # El payload exacto como lo armabas en tu poc_api_yapp.py
    payload = f'{{"products":[{{"id":"{id_producto}","result_id":""}}],"coords":{{"lat":{lat},"lng":{lng}}},"commune_id":10101}}'

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, data=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error al cotizar en YAPP"
            )

        try:
            data = response.json()
            farmacias = data.get("data", [])

            # Ordenamos las farmacias por precio y distancia como en tu yapp_service.py
            con_distancia = [
                p for p in farmacias if p.get("pharmacy_distance") is not None
            ]
            sin_distancia = [p for p in farmacias if p.get("pharmacy_distance") is None]

            con_distancia.sort(
                key=lambda x: (x.get("pharmacy_distance", 999), x.get("total", 999))
            )
            sin_distancia.sort(key=lambda x: x.get("total", 999))

            return {"data": con_distancia + sin_distancia}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
