import re
import json
import logging
import requests
from bs4 import BeautifulSoup

from datetime import datetime

CONSTANTES = json.load(open("constantes.json","r", encoding="utf-8"))
CLASES = CONSTANTES["CLASES"]

def find_id(text):
    pattern = r'-(\w{32})#'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def get_content(link_fecha, country):
    url = link_fecha[0]
    fecha = link_fecha[1]

    """
    La función toma todos los datos de una oferta dada su url.
    """
    querystring = {"responsive": "true"}

    data = dict()

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    } 

    response = requests.request("GET", url, data="", headers=headers, params=querystring)


    if not response.ok:
        logging.error(f"Error al obtener datos de {url} - status: {response.status_code}")
        return False

    try:

        soup = BeautifulSoup(response.text, "html.parser")

        data['Plataforma'] = "Computrabajo"

        # Ubicacion + Nombre empresa
        main_element = soup.find('main')
        container_div = main_element.find('div', class_='container')
        name_jobLoc_raw = container_div.find("p",{"class":CLASES["name_jobLoc"]})
        name_jobLoc = name_jobLoc_raw.text if name_jobLoc_raw else None
        data["ubicacion"] = name_jobLoc.split("-")[-1].strip() if name_jobLoc else None
        data["Nombre empresa"]="-".join(name_jobLoc.split("-")[:-1]).strip() if name_jobLoc else None

         # Descripcion de la empresa
        desc_empresa = soup.find("p", {"show-more": True}) 
        data["Descripción de la empresa"] = desc_empresa.get_text() if desc_empresa else None

        data["Industria de la empresa"] = ""
        
        # # Fecha de publicacion
        data["Fecha publicación"] = fecha

        # Link de la oferta
        data["Link a la búsqueda"] = url
        
        # Titulo de la oferta
        titulo = soup.find("h1",{"class":CLASES["titulo"]})
        data["Titulo de puesto"] = titulo.text if titulo else None

         # Descripcion de la oferta
        raw_descr = soup.find_all("p",{"class":CLASES["descripcion"]})
        data["Descripción del puesto"]= raw_descr[0].get_text() if raw_descr and raw_descr[0] else None

        # Requisitos 
        raw_req = soup.find("ul",{"class":CLASES["requisitos"]})
        data["Requisitos"] = raw_req.get_text() if raw_req else None

        data["Experiencia"] = ""
        
        # Tags (salario, Jornada, tipo de contrato)
        tags_raw = soup.find_all("span", {"class": CLASES["tags"]})
        salario_jornada_contrato = list(set([tag.text for tag in tags_raw ])) if tags_raw else None
        
        # Detectar salario
        def contar_numeros(texto):
            # Buscar números en el texto, incluyendo posibles símbolos de moneda como US$ y otros caracteres adicionales
            return len(re.findall(r'\d+(?:\.\d+)?(?:\s*[A-Za-z$]+)?', texto)) > 2
       
        # clasificar
        for elemento in salario_jornada_contrato:
            if 'contrato' in elemento.lower():
                data['Tipo de contrato'] = elemento
            elif 'tiempo' in elemento.lower():
                data['Jornada'] = elemento
            elif contar_numeros(elemento) > 1:
                data['Salario'] = elemento
            else:
                data['Modalidad'] = elemento
        

        # Palabras clave
        pal = soup.find("p",{"class":CLASES["palabras_clave"]})
        data["Palabras clave"]= pal.get_text() if pal else None

        # Pais
        data["País"] = country

        # Localidad
        data["Localidad"] = data['ubicacion'].split(",")[0].strip() if data['ubicacion'] else None

        # Provincia
        data["Provincia"] = data['ubicacion'].split(",")[-1].strip() if data['ubicacion'] else None

        data.pop('ubicacion', None) 

        # Educación 
        data['Educación'] = ""

        if data["Titulo de puesto"] is None or not url:
            return False
        
    except Exception as e:
        logging.error(f"ERROR: {e}")
            
    return data
