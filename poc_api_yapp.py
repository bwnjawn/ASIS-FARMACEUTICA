import requests


def buscador_interactivo_yapp():
    print("==================================================")
    print("💊 BUSCADOR INTERACTIVO DE FARMACIAS (PUERTO MONTT)")
    print("==================================================\n")

    nombre_medicamento = input("Escribe el medicamento a buscar (ej. Paracetamol): ")
    print(f"\n🔍 1. Buscando todas las coincidencias para '{nombre_medicamento}'...\n")

    headers = {
        "accept": "*/*",
        "accept-language": "es-ES,es;q=0.9",
        # Asegúrate de que este token siga vigente, si da error 401, actualízalo desde tu navegador
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijc5OTRiNGYzMTU2MzJiMjk3NzAwNmQ5M2U5NGIyYWNiZTMwNWZlNDYiLCJ0eXAiOiJKV1QifQ.eyJwcm92aWRlcl9pZCI6ImFub255bW91cyIsImlzcyI6Imh0dHBzOi8vc2VjdXJldG9rZW4uZ29vZ2xlLmNvbS95YXBwLWUyNTE2IiwiYXVkIjoieWFwcC1lMjUxNiIsImF1dGhfdGltZSI6MTc4MDg5NTQ2MiwidXNlcl9pZCI6Ik1xN2xNSm92ZXFkeWFmZGtCQkRvZG95cU9nSTIiLCJzdWIiOiJNcTdsTUpvdmVxZHlhZmRrQkJEb2RveXFPZ0kyIiwiaWF0IjoxNzgwODk1NDYyLCJleHAiOjE3ODA4OTkwNjIsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnt9LCJzaWduX2luX3Byb3ZpZGVyIjoiYW5vbnltb3VzIn19.NjGS3cLYnDDSlB6xlkncQUvN3X5p3N6D5lgq3wi2IIZAArJlb-TdSrdaaNJ3jl128SjZaaBexvaZJRrPfHlZJPTKBmfO7vMcJ3EwQL-dhR4bGwfzYWpQbNsFE20iHrpeQ_S9MI7FkkU9fMsYcAxAtVQJ0AoGiGWNKoF97uKS0L-oPXddlZoYErV8n0bzkuWOCKfEwXK7TvyigI6Qdy1gk_8w0xLd2HF1RwGtg2-jaUdw2QIyzRRTrN0yFjfQYQbyHkQyXUGpfKx-942W-HpGBhxnNAzTXIREkDrg1oLCE1CS2RbLJYdbEyKMQInix06LD2dNpxI_ZQfl-OkzF84xmQ",
        "client-id": "f54834cd-e9b3-11eb-a606-067f",
        "content-type": "text/plain;charset=UTF-8",
        "origin": "https://web.yapp.cl",
        "referer": "https://web.yapp.cl/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }

    try:
        # --- PASO 1: OBTENER TODOS LOS RESULTADOS ---
        url_search = "https://api-integration.yapp.cl/v2/vademecum/autocomplete"
        params = {"text": nombre_medicamento, "external_vademecum": "0"}

        res_search = requests.get(url_search, params=params, headers=headers)

        if res_search.status_code != 200:
            print(f"❌ Error del servidor: {res_search.status_code}")
            return

        resultados = res_search.json().get("data", [])

        # Guardamos TODOS los productos válidos en una lista
        productos_encontrados = []
        for item in resultados:
            if item.get("product_id"):
                productos_encontrados.append(item)

        if not productos_encontrados:
            print(
                f"⚠️ No se encontró ningún medicamento relacionado con '{nombre_medicamento}'."
            )
            return

        # Imprimimos los primeros 10 resultados para que el usuario elija
        print(
            f"📦 Se encontraron {len(productos_encontrados)} opciones. Mostrando las primeras 10:\n"
        )

        # Limite visual para la consola
        limite = min(74, len(productos_encontrados))
        for i in range(limite):
            nombre_prod = productos_encontrados[i].get("product_name", "Sin nombre")
            # Extraemos el laboratorio para dar más contexto
            lab = productos_encontrados[i].get("laboratory_name", "")
            print(f"  [{i + 1}] {nombre_prod} ({lab})")

        print("-" * 50)

        # Esperamos a que el usuario escriba un número
        seleccion = input(
            "\n👉 Ingresa el NÚMERO del medicamento que quieres cotizar (o 'x' para salir): "
        )

        if seleccion.lower() == "x":
            return

        indice = int(seleccion) - 1

        if indice < 0 or indice >= limite:
            print("❌ Número inválido.")
            return

        # --- PASO 2: COTIZAR EL PRODUCTO ELEGIDO ---
        producto_elegido = productos_encontrados[indice]
        producto_id = producto_elegido.get("product_id")
        nombre_oficial = producto_elegido.get("product_name")

        print(f"\n⏳ 2. Cotizando '{nombre_oficial}' en Puerto Montt...\n")

        url_quote = "https://api-integration.yapp.cl/v2/quotation"
        lat_pto_montt = -41.4693
        lng_pto_montt = -72.9424

        payload_dinamico = f'{{"products":[{{"id":"{producto_id}","result_id":""}}],"coords":{{"lat":{lat_pto_montt},"lng":{lng_pto_montt}}},"commune_id":10101}}'

        res_quote = requests.post(url_quote, data=payload_dinamico, headers=headers)

        if res_quote.status_code == 200:
            farmacias = res_quote.json().get("data", [])

            if not farmacias:
                print(
                    "⚠️ No hay stock registrado de este producto exacto en las farmacias cercanas."
                )
                return

            print("🏥 ¡Listo! Opciones encontradas:\n")
            for farmacia in farmacias:
                nombre_farm = farmacia.get("pharmacy_chain_name", "Desconocida")
                precio = farmacia.get("total", "N/A")
                distancia = farmacia.get("pharmacy_distance", "N/A")

                dist_str = (
                    f"a {distancia:.1f} km"
                    if isinstance(distancia, (int, float))
                    else "distancia no disponible"
                )
                print(f"   ✅ {nombre_farm}: ${precio} ({dist_str})")
        else:
            print(f"❌ Error al cotizar: {res_quote.status_code}")

    except Exception as e:
        print(f"🚨 Error: {e}")


if __name__ == "__main__":
    buscador_interactivo_yapp()
