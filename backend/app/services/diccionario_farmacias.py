import logging
import math

logger = logging.getLogger(__name__)

# ==========================================
# 1. BASE DE DATOS LOCAL DE SUCURSALES (PUERTO MONTT)
# ==========================================
# Nota: Los 'chain_id' (1, 2, 3...) son los identificadores más comunes
# para las grandes cadenas en sistemas chilenos. Si al probar vemos que
# YAPP usa otros, solo actualizamos este número.

SUCURSALES_PUERTO_MONTT = {
    # Cruz Verde (Asumiremos ID 2 por ahora)
    2: [
        {
            "nombre_local": "Cruz Verde - Mall Paseo Costanera",
            "direccion": "Illapel 10, Nivel 1",
            "lat": -41.4725,
            "lng": -72.9405,
        },
        {
            "nombre_local": "Cruz Verde - Centro Histórico",
            "direccion": "Antonio Varas 445",
            "lat": -41.4687,
            "lng": -72.9412,
        },
        {
            "nombre_local": "Cruz Verde - Terminal de Buses",
            "direccion": "Av. Diego Portales 1001",
            "lat": -41.4718,
            "lng": -72.9348,
        },
    ],
    # Salcobrand (Asumiremos ID 3)
    3: [
        {
            "nombre_local": "Salcobrand - Paseo del Mar",
            "direccion": "Urmeneta 580",
            "lat": -41.4695,
            "lng": -72.9418,
        },
        {
            "nombre_local": "Salcobrand - Centro",
            "direccion": "Antonio Varas 688",
            "lat": -41.4678,
            "lng": -72.9425,
        },
    ],
    # Farmacias Ahumada (Asumiremos ID 1)
    1: [
        {
            "nombre_local": "Farmacias Ahumada - Plaza de Armas",
            "direccion": "Pedro Montt 114",
            "lat": -41.4699,
            "lng": -72.9400,
        },
        {
            "nombre_local": "Farmacias Ahumada - Paseo Talca",
            "direccion": "Talca 74",
            "lat": -41.4705,
            "lng": -72.9410,
        },
    ],
    # Farmacias Dr. Simi (Asumiremos ID 4)
    4: [
        {
            "nombre_local": "Dr. Simi - Mercado Angelmó",
            "direccion": "Av. Angelmó 1856",
            "lat": -41.4822,
            "lng": -72.9495,
        },
        {
            "nombre_local": "Dr. Simi - Centro Varas",
            "direccion": "Antonio Varas 810",
            "lat": -41.4670,
            "lng": -72.9430,
        },
    ],
}


# ==========================================
# 2. MOTOR DE CÁLCULO DE DISTANCIA (FÓRMULA HAVERSINE)
# ==========================================
def calcular_distancia_metros(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """
    Calcula la distancia en metros entre dos coordenadas GPS.
    """
    R = 6371000  # Radio de la Tierra en metros
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# ==========================================
# 3. INTERCEPTOR Y BUSCADOR LOCAL
# ==========================================
def inyectar_ubicaciones_locales(
    farmacia_yapp: dict, lat_usuario: float, lng_usuario: float
) -> list:
    """
    Toma los datos de YAPP, busca TODAS las sucursales de esa cadena en Puerto Montt
    y genera una copia del resultado para cada local físico.
    """
    chain_id = farmacia_yapp.get("pharmacy_chain_id")
    chain_name = farmacia_yapp.get("pharmacy_chain_name", "Farmacia")

    # Fallback si el ID no cuadra
    if chain_id not in SUCURSALES_PUERTO_MONTT:
        nombre_lower = str(chain_name).lower()
        if "cruz verde" in nombre_lower:
            chain_id = 2
        elif "salcobrand" in nombre_lower:
            chain_id = 3
        elif "ahumada" in nombre_lower:
            chain_id = 1
        elif "simi" in nombre_lower:
            chain_id = 4
        else:
            # Si no la conocemos, la devolvemos tal cual dentro de una lista
            return [farmacia_yapp]

    sucursales_locales = SUCURSALES_PUERTO_MONTT[chain_id]
    resultados_multiplicados = []

    # Por cada sucursal local de esta cadena, creamos una copia exacta con los precios
    # pero le inyectamos la ubicación específica de este local.
    for sucursal in sucursales_locales:
        dist = calcular_distancia_metros(
            lat_usuario, lng_usuario, sucursal["lat"], sucursal["lng"]
        )

        # OJO AQUÍ: Usamos .copy() para no sobreescribir los datos de las otras sucursales
        farmacia_clon = farmacia_yapp.copy()
        farmacia_clon["pharmacy_chain_name"] = sucursal["nombre_local"]
        farmacia_clon["pharmacy_address"] = sucursal["direccion"]
        farmacia_clon["pharmacy_latitude"] = sucursal["lat"]
        farmacia_clon["pharmacy_longitude"] = sucursal["lng"]
        farmacia_clon["pharmacy_distance"] = int(dist)
        farmacia_clon["es_ubicacion_local"] = True

        resultados_multiplicados.append(farmacia_clon)

    return resultados_multiplicados
