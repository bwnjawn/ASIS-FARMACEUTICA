from app.services.diccionario_farmacias import inyectar_ubicaciones_locales
from app.services.yapp_scraper import obtener_token_actual, renovar_token_yapp
from curl_cffi.requests import AsyncSession
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/medicamentos", tags=["Medicamentos (YAPP)"])

# Cabeceras clonadas de tu éxito en PowerShell
YAPP_HEADERS_PERFECTOS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "es-ES,es;q=0.9,haw;q=0.8,mt;q=0.7",
    "client-id": "f54834cd-e9b3-11eb-a606-067f",
    "origin": "https://web.yapp.cl",
    "priority": "u=1, i",
    "referer": "https://web.yapp.cl/",
    "request-from": "medication-buy",
    "sec-ch-ua": '"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"iOS"',
}


@router.get("/buscar")
async def buscar_medicamento(
    q: str = Query(..., description="Nombre del medicamento a buscar"),
):
    token = obtener_token_actual()
    if not token:
        token = await renovar_token_yapp()
        if not token:
            raise HTTPException(
                status_code=503, detail="Servicio temporalmente no disponible."
            )

    # Paso 1: Sincronizar el Endpoint de Búsqueda
    url = f"https://api-integration.yapp.cl/v2/vademecum/autocomplete?text={q}&external_vademecum=0&commune_id=10101"

    # Paso 3: Sanitizar la inyección del Token (asumiendo que viene limpio del scraper)
    headers = {**YAPP_HEADERS_PERFECTOS, "authorization": f"Bearer {token}"}

    async with AsyncSession(impersonate="chrome120") as client:
        response = await client.get(url, headers=headers)

        if response.status_code in [401, 403]:
            print("⚠️ Token vencido o Firewall alerta (403/401). Renovando...")
            nuevo_token = await renovar_token_yapp()
            if nuevo_token:
                headers["authorization"] = f"Bearer {nuevo_token}"
                response = await client.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Error de comunicación con el catálogo.",
            )

        return response.json()


@router.get("/cotizar")
async def cotizar_medicamento(
    id_producto: str = Query(..., description="ID del producto de YAPP (ej. '12345')"),
    lat: float = Query(-41.4693, description="Latitud (Por defecto Puerto Montt)"),
    lng: float = Query(-72.9424, description="Longitud (Por defecto Puerto Montt)"),
):
    """
    Endpoint para cotizar un medicamento específico.
    Inyecta la geolocalización local desde diccionario_farmacias.py.
    """
    token = obtener_token_actual()
    if not token:
        raise HTTPException(status_code=503, detail="Token no disponible")

    url = "https://api-integration.yapp.cl/v2/quotation"
    headers = {**YAPP_HEADERS_PERFECTOS, "authorization": f"Bearer {token}"}

    # Construcción exacta del payload requerido por YAPP
    payload = f'{{"products":[{{"id":"{id_producto}","result_id":""}}],"coords":{{"lat":{lat},"lng":{lng}}},"commune_id":10101}}'

    # También protegemos este endpoint con curl_cffi para máxima seguridad
    async with AsyncSession(impersonate="chrome120") as client:
        response = await client.post(url, data=payload, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Error al cotizar en YAPP"
            )

        try:
            data = response.json()
            farmacias_brutas = data.get("data", [])

            farmacias_cercanas = []
            RADIO_MAXIMO_METROS = 10000  # 10 kilómetros a la redonda

            for f_bruta in farmacias_brutas:
                # Interceptamos la respuesta inyectando nuestro motor geográfico local
                sucursales_mejoradas = inyectar_ubicaciones_locales(f_bruta, lat, lng)

                for f_mejorada in sucursales_mejoradas:
                    distancia = f_mejorada.get("pharmacy_distance")

                    # Filtro final: Si no tiene distancia válida o supera los 10km, se descarta
                    if distancia is not None and distancia <= RADIO_MAXIMO_METROS:
                        farmacias_cercanas.append(f_mejorada)

            # Ordenamos por precio total de menor a mayor, y de estar igual precio, por cercanía
            farmacias_cercanas.sort(
                key=lambda x: (
                    x.get("total", 999999),
                    x.get("pharmacy_distance", 99999),
                )
            )

            return {"data": farmacias_cercanas}

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error procesando datos: {str(e)}"
            )
