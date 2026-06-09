from fastapi import APIRouter, HTTPException, Query, Header
from typing import Optional
from app.services.yapp_service import search_medications, get_quotation

router = APIRouter()


@router.get("/medicamentos/buscar")
async def buscar_medicamentos(
    q: str = Query(..., min_length=2, description="Nombre del medicamento o principio activo"),
    authorization: Optional[str] = Header(None),
):
    """
    RF01: Búsqueda de medicamentos por nombre comercial o principio activo.
    Retorna lista de productos con tolerancia a errores tipográficos (manejo en YAPP).
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Se requiere token de autorización YAPP. Incluye el header 'Authorization: Bearer <token>'"
        )

    token = authorization.replace("Bearer ", "")

    try:
        results = await search_medications(text=q, auth_token=token)
        return {
            "query": q,
            "total": len(results),
            "results": [
                {
                    "product_id": item.get("product_id"),
                    "product_name": item.get("product_name"),
                    "formula_name": item.get("formula_name"),
                    "laboratory_name": item.get("laboratory_name"),
                    "presentation": item.get("presentation"),
                    "prescription": item.get("prescription"),
                    "minimal_price": item.get("minimal_price"),
                    "product_logo": item.get("product_logo"),
                    "category": item.get("category"),
                }
                for item in results[:20]
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error al conectar con servicio de medicamentos: {str(e)}")


@router.get("/medicamentos/{product_id}/cotizar")
async def cotizar_medicamento(
    product_id: str,
    lat: Optional[float] = Query(None, description="Latitud del usuario"),
    lng: Optional[float] = Query(None, description="Longitud del usuario"),
    authorization: Optional[str] = Header(None),
):
    """
    RF02: Cotización de precios en farmacias ordenada por geolocalización.
    Retorna lista de farmacias ordenadas por cercanía y precio.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Se requiere token de autorización YAPP"
        )

    token = authorization.replace("Bearer ", "")

    try:
        pharmacies = await get_quotation(
            product_id=product_id,
            auth_token=token,
            lat=lat,
            lng=lng,
        )

        if not pharmacies:
            return {
                "product_id": product_id,
                "total_pharmacies": 0,
                "pharmacies": [],
                "message": "No hay stock disponible en farmacias cercanas",
            }

        return {
            "product_id": product_id,
            "total_pharmacies": len(pharmacies),
            "pharmacies": [
                {
                    "name": p.get("pharmacy_chain_name"),
                    "logo": p.get("pharmacy_chain_logo"),
                    "total": p.get("total"),
                    "distance_km": p.get("pharmacy_distance"),
                    "address": p.get("pharmacy_address"),
                    "hours": p.get("pharmacy_hours"),
                    "available": p.get("pharmacy_chain_available"),
                    "url": p.get("pharmacy_chain_url"),
                    "online": p.get("pharmacy_chain_online", 0),
                }
                for p in pharmacies
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error al cotizar: {str(e)}")
