import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Cargamos las variables de tu archivo .env
load_dotenv()

URL: str = os.environ.get("SUPABASE_URL")
KEY: str = os.environ.get("SUPABASE_KEY")

if not URL or not KEY:
    raise ValueError("Faltan las credenciales de Supabase en el archivo .env")

# Inicializamos el cliente oficial
supabase: Client = create_client(URL, KEY)
