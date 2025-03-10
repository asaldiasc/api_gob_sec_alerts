import requests
import json

# URL base de la API
BASE_URL = "https://csirt.gob.cl/api/v1/alerts/?page=1"

def obtener_alertas():
    try:
        # Haciendo la solicitud GET
        response = requests.get(BASE_URL)
        print(f"🔹 Código de estado: {response.status_code}")

        if response.status_code == 200:
            datos = response.json()  # Convertir la respuesta a JSON
            
            # Verificar si la clave "items" existe y contiene datos
            alertas = datos.get("items", [])

            if not alertas:
                print("⚠️ No se encontraron alertas disponibles.")
                return []
            
            # Estructurar las alertas en un formato JSON más claro
            alertas_estructuradas = []
            for alerta in alertas:
                alerta_json = {
                    "id": alerta.get("code"),
                    "titulo": alerta.get("title"),
                    "fecha": alerta.get("date"),
                    "categoria": alerta.get("category"),
                    "tipo_incidente": alerta.get("incident_type"),
                    "nivel_riesgo": alerta.get("tlp", "Desconocido"),
                    "descripcion_general": alerta.get("general_description"),
                    "descripcion_detallada": alerta.get("specific_description"),
                    "productos_afectados": [
                        producto["name"] for producto in alerta.get("vulnerable_products", [])
                    ],
                    "vulnerabilidades": [
                        {
                            "cve": vuln["code"],
                            "url": vuln["url"]
                        } for vuln in alerta.get("vulnerabilities", [])
                    ],
                    "fuente": "CSIRT Gobierno",
                    "url_detalle": next((link["url"] for link in alerta.get("related_links", [])), "No disponible")
                }
                alertas_estructuradas.append(alerta_json)

            return alertas_estructuradas
        else:
            print(f"❌ Error en la solicitud: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error al conectarse a la API: {e}")
        return None

# Ejecutar y mostrar alertas en formato JSON estructurado
alertas = obtener_alertas()
if alertas:
    print(json.dumps(alertas, indent=4, ensure_ascii=False))  # Imprimir JSON formateado
else:
    print("⚠️ No se encontraron alertas disponibles.")
