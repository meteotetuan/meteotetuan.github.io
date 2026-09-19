import os
import requests
import json

# 1. Traer los secretos guardados de GitHub
API_KEY = os.environ.get("WEATHERLINK_API_KEY")
API_SECRET = os.environ.get("WEATHERLINK_API_SECRET")
STATION_ID = os.environ.get("WEATHERLINK_STATION_ID")

# 2. Dirección oficial de la API v2 para tu estación
url = f"https://api.weatherlink.com/v2/current/{STATION_ID}"

# 3. Enviar la API Key como parámetro normal de consulta
params = {
    "api-key": API_KEY
}

# 4. Enviar la API Secret oculta de forma segura en las cabeceras (Método Oficial)
headers = {
    "X-Api-Secret": API_SECRET
}

print("Conectando correctamente con WeatherLink v2...")

# 5. Hacer la llamada al servidor enviando tanto parámetros como cabeceras
response = requests.get(url, params=params, headers=headers)

# 6. Guardar los datos si la conexión es exitosa
if response.status_code == 200:
    datos_clima = response.json()
    
    with open("clima.json", "w", encoding="utf-8") as archivo:
        json.dump(datos_clima, archivo, indent=4, ensure_ascii=False)
        
    print("¡Éxito! Datos guardados correctamente en clima.json")
else:
    print(f"Error del servidor. Código de estado: {response.status_code}")
    print(response.text)
    exit(1)
