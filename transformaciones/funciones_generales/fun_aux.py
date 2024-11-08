import json

# Cargar diccionario JSON
def obtener_json(ruta):
    with open(ruta, encoding='utf-8-sig') as archivo:
        DICCIONARIO = json.load(archivo)
        return DICCIONARIO