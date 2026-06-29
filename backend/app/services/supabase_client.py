import os

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    raise Exception("Faltan las credenciales de Supabase en el archivo .env")

# Cliente global de Supabase para usar en toda la app
supabase: Client = create_client(URL, KEY)
