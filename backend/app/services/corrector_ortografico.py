import logging

from thefuzz import process

logger = logging.getLogger(__name__)

# Diccionario en memoria de los principios activos y marcas más comunes
# en el uso geriátrico y general. Puedes expandir esta lista iterativamente.
MEDICAMENTOS_COMUNES = [
    "paracetamol",
    "ibuprofeno",
    "losartan",
    "eutirox",
    "ketorolaco",
    "aspirina",
    "omeprazol",
    "atorvastatina",
    "metformina",
    "enalapril",
    "amoxicilina",
    "azitromicina",
    "diclofenaco",
    "naproxeno",
    "tramadol",
    "pregabalina",
    "celecoxib",
    "clonazepam",
    "alprazolam",
    "sertralina",
    "levotiroxina",
    "hidroclorotiazida",
    "amlodipino",
    "valsartan",
]


def corregir_medicamento(busqueda_usuario: str, umbral_similitud: int = 75) -> str:
    """
    Compara la búsqueda del usuario con el diccionario local.
    Si la coincidencia supera el umbral (ej. 75%), devuelve el término corregido.
    De lo contrario, asume que es un medicamento que no tenemos mapeado y lo deja pasar.
    """
    if not busqueda_usuario:
        return busqueda_usuario

    busqueda_limpia = busqueda_usuario.lower().strip()

    # process.extractOne devuelve una tupla: ("palabra_coincidente", puntaje)
    mejor_coincidencia, puntaje = process.extractOne(
        busqueda_limpia, MEDICAMENTOS_COMUNES
    )

    if puntaje >= umbral_similitud:
        if busqueda_limpia != mejor_coincidencia:
            logger.info(
                f"🔧 Autocorrección difusa: '{busqueda_usuario}' -> '{mejor_coincidencia}' (Certeza: {puntaje}%)"
            )
        return mejor_coincidencia

    # Si no superó el umbral, devolvemos lo que el usuario escribió originalmente
    return busqueda_usuario
