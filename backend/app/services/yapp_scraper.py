import logging

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

# Variable global que guardará el token en la memoria RAM del servidor
CURRENT_YAPP_TOKEN = None


async def renovar_token_yapp():
    """
    Inicia un navegador invisible, entra a YAPP y captura el token de sesión.
    """
    global CURRENT_YAPP_TOKEN

    logger.info("Iniciando bot de Playwright para renovar Token de YAPP...")

    async with async_playwright() as p:
        # Lanzamos Chromium en modo headless (invisible)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # Función para interceptar las peticiones de red
        async def interceptar_peticion(request):
            global CURRENT_YAPP_TOKEN
            headers = request.headers
            # Buscamos el header de autorización que manda la página al buscar
            if "authorization" in headers and "Bearer" in headers["authorization"]:
                nuevo_token = headers["authorization"].replace("Bearer ", "")
                CURRENT_YAPP_TOKEN = nuevo_token
                logger.info("✅ ¡Token de YAPP capturado exitosamente!")

        # Escuchamos todas las peticiones de la página
        page.on("request", interceptar_peticion)

        try:
            # Entramos a la web
            await page.goto("https://web.yapp.cl", wait_until="domcontentloaded")

            # Simulamos una pequeña espera o interacción para que la web genere el token
            await page.wait_for_timeout(3000)

        except Exception as e:
            logger.error(f"Error al obtener el token: {str(e)}")
        finally:
            await browser.close()

    return CURRENT_YAPP_TOKEN


def obtener_token_actual():
    """Devuelve el token guardado en memoria para usarlo en los controladores."""
    return CURRENT_YAPP_TOKEN
