import json
import logging
import pandas as pd
from links.get_links import get_links
from content.get_content import get_content
from links.get_localidades import get_localidades

import os

if not os.path.exists("../../bbdd"):
    os.mkdir("../../bbdd")

if not os.mkdir("../../bbdd/backup"):
    os.path.exists("../../bbdd/backup")


logging.basicConfig(format='[%(asctime)s - %(filename)15s:%(lineno)s - %(funcName)18s()] - %(levelname)s: %(message)s', level=logging.INFO)

CONSTANTES = json.load(open("constantes.json","r", encoding="utf-8"))

df_compu = []

for country in CONSTANTES["DATA_PAISES"].keys():
    localidades = get_localidades(country)

    # # Obtengo los ids existentes por pais
    # ids_existentes = get_ids(country)

    for localidad, endpoint in localidades.items():
        links_ofertas = []
        logging.info(f"Obteniendo links de ofertas de {localidad}, {country}")
        links_ofertas_iter = get_links(country, endpoint_localidad=endpoint)
        if links_ofertas_iter == False:
            logging.error(f"Error al obtener links de ofertas de {localidad}, {country}")
        else:
            links_ofertas.extend(links_ofertas_iter)

        # links_ofertas = [link for link in links_ofertas if link not in ids_existentes]

        data = []
        for index, link_fecha in enumerate(links_ofertas):
            logging.info(f"Obteniendo oferta {index}/{len(links_ofertas)}")
            contenido = get_content(link_fecha, country)
            data.append(contenido)

        logging.info("Ofertas con errores: {}".format(sum([d for d in data if d is False])))

        df = pd.DataFrame([d for d in data if d is not False])
        # df["country"] = country
        df_compu.append(df)
    
df_concatenado = pd.concat(df_compu)
df_concatenado.to_excel("../../bbdd/compucrudo.xlsx", index=False)
