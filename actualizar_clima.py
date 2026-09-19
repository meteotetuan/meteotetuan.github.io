import os
import time
import hmac
import hashlib
import requests
import json

# 1. Leer las contraseñas secretas que guardamos en GitHub
API_KEY = os.environ.get("WEATHERLINK_API_KEY")
API_SECRET = os.environ.get("WEATHERLINK_API_SECRET")
STATION_ID = os.environ.get("WEATHERLINK_STATION_ID")

# 2. Configurar la hora actual para la firma de seguridad de Davis
timestamp = str(int(time.time()))

# 3. Preparar los datos que le vamos a pedir a la API v2
params = {
    "api-key": API_KEY,
    "t": timestamp
}

# La API v2 exige ordenar los parámetros alfabéticamente para crear la firma
msg = f"api-key{API_KEY}station-id{STATION_ID}t{timestamp}"

# 4. Crear la firma digital matemática usando tu API Secret
api_signature = hmac.new(
    API_SECRET.encode('utf-8'),
    msg.encode('utf-8'),
    hashlib.sha256
).hexdigest()

# 5. Añadir la firma a los parámetros de la consulta
params["api-signature"] = api_signature

# 6. Hacer la llamada real a los servidores de WeatherLink
url = f"https://weatherlink.com{STATION_ID}"
print("Conectando con WeatherLink v2...")
response = requests.get(url, params=params)

# 7. Si todo sale bien, guardar los datos en un archivo llamado clima.json
if response.status_code == 200:
    datos_clima = response.json()
    
    with open("clima.json", "w", encoding="utf-8") as archivo:
        json.dump(datos_clima, archivo, indent=4, ensure_ascii=False)
        
    print("¡Datos descargados con éxito y guardados en clima.json!")
else:
    print(f"Error al conectar con la API. Código de error: {response.status_code}")
    print(response.text)
    exit(1)
