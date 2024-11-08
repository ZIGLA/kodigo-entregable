import json
import logging
import requests
from bs4 import BeautifulSoup

CONSTANTES = json.load(open("constantes.json","r", encoding="utf-8"))

def get_links(country:str, endpoint_localidad:str):
    """
    La función obtiene todos los links de las ofertas de empleo para un determinado país y localidad.
    """
    URL = CONSTANTES["DATA_PAISES"][country]["URL"]

    headers = CONSTANTES["HEADERS"]
    headers["authority"] = URL
    headers["origin"] = f"https://{URL}"
    headers["referer"] = f"https://{URL}/"

    page = 1
    lista_links = []
    
    while True:
        response = requests.request("GET", f"https://{URL}{endpoint_localidad}?pubdate=7&p={page}", json="", headers=headers, params={})
        if not response.ok:
            if response.status_code == 404:
                break
            logging.error(f"Error al obtener los registros de la página {page} - codigo {response.status_code}")
            lista_links = False
            break
        else:
            logging.info(f"Obteniendo links de página {page}")
            soup = BeautifulSoup(response.text, "html.parser")
            links_raw = soup.find_all("a", {"class":CONSTANTES["CLASES"]["links_ofertas"]}, href=True)
            date = soup.find_all("p", {"class":CONSTANTES["CLASES"]["date"]})
            if links_raw and date:
                for link, date_element in zip(links_raw, date):
                    fecha = date_element.get_text(strip=True)
                    enlace_completo = f"https://{URL}"+link["href"]
                    link_fecha = (enlace_completo, fecha)
                    lista_links.append((link_fecha))
                page += 1
            else:
                logging.info(f"{page} páginas obtenidas")
                break
    return lista_links