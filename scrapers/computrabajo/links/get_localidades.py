import json
import requests

CONSTANTES = json.load(open("constantes.json","r", encoding="utf-8"))

def get_localidades(country):
    # Obtengo la url base segun el pais
    URL_BASE = CONSTANTES["DATA_PAISES"][country]["URL"]

    url = f"https://{URL_BASE}/ajax/geticonplacessuggest"
    headers = CONSTANTES["HEADERS"]
    
    headers["authority"] = URL_BASE
    headers["origin"] = f"https://{URL_BASE}"
    headers["referer"] = f"https://{URL_BASE}/"

    data = {"q": ""}

    response = requests.post(url, headers=headers, data=data)

    localidades = dict()
    for loc in response.json():
        localidades[loc["Title"]] = loc["Url"]
    return localidades