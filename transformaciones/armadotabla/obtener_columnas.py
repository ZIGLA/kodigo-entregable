import pandas as pd
import json
import ast

"""
Transformacion del scrapping de tecoloco a tabla cruda
"""

"""
Funciones
"""
# Acomoda los datos de JobPostingSchema para podes vincularlo con los datos de digital data
def reordenar(x):
    aux = x

    # hiringOrganization
    for key, value in x["hiringOrganization"].items():
        aux[f"hiringOrganization - {key}"] = value

    # jobLocation
    aux["jobLocation - type"] = x["jobLocation"]["@type"]

    for key, value in x["jobLocation"]["address"].items():
        aux[f"joblocation - address - {key}"] = value

    for key, value in x["jobLocation"]["geo"].items():
        aux[f"joblocation - geo - {key}"] = value

    # baseSalary
    aux["baseSalary - type"] = x["baseSalary"]["@type"]
    aux["baseSalary - currency"] = x["baseSalary"]["currency"]

    aux["baseSalary - value - type"] = x["baseSalary"]["value"]["@type"]
    aux["baseSalary - value - minValue"] = x["baseSalary"]["value"]["minValue"]
    aux["baseSalary - value - maxValue"] = x["baseSalary"]["value"]["maxValue"]

    aux.pop('hiringOrganization', None)
    aux.pop('jobLocation', None)
    aux.pop('baseSalary', None)

    return aux

# Obtiene las columnas y los datos a partir de los diccionarios de las columnas digitalData y jobpostingSchema
def procesar(x):
    try:
        digitalData = json.loads(x['digitalData']) if not pd.isna(x["digitalData"]) else None
    except:
        digitalData = None
    try:
        jobPostingSchema =  json.loads(x['jobPostingSchema']) if not pd.isna(x["jobPostingSchema"]) else None
    except:
        jobPostingSchema = None
    ret = None
    # 3 opciones de salida: vincula los diccionarios o retorna el que tiene los datos si el otro es nulo.
    if digitalData is not None and jobPostingSchema is not None:
        digitalData.update(reordenar(dict(jobPostingSchema)))
        ret = digitalData
    elif digitalData is not None:
        ret = dict(digitalData)
    elif jobPostingSchema is not None:
        ret = dict(jobPostingSchema)
    else:
        ret = None
    return ret

"""
Procesamiento de columna details
"""
def columna_details(df):
# Evaluar si es un diccionario details, armado y rellenado de columnas a partir de details
    df["details"] = df["details"].apply(ast.literal_eval)

    columnas_details = ['Puestos Vacantes', 'País', 'Cargo Solicitado', 'Nivel de Experiencia', 'Salario máximo (USD)', 'Edad', 'Vehículo', 'Género', '(Base de datos)', 'Departamento', 'Área de la Empresa', 'Salario minimo (USD)', 'Tipo de Contratación']
    for columna in columnas_details:
        df[columna] = ""

    for columna in columnas_details:
        df[columna] = df["details"].apply(lambda x: x[columna] if columna in x.keys() else "")

    # df.to_excel("test/T1-columnasdetails.xlsx")
    # details = df
    return df

""" 
Procesamiento de columnas JobPostingSchema y DigitalData
"""
def columna_JobDigital(df):
    df = df[df["digitalData"] != '{\'Error\': \'error\'}']
    df["datoCompleto"] = df.apply(lambda x: procesar(x), axis=1)

   
    for indice, elemento in enumerate(df['datoCompleto']):
        if pd.isnull(elemento):
            print(indice)
            df.at[indice, 'datoCompleto'] = {"N/A":"N/A"}

    df_JobDigital = pd.DataFrame.from_records(list(df['datoCompleto']))
    return df_JobDigital
"""
Funcion principal: Obtener las columnas de las variables a partir de las columnas “Details”, “JobPostingSchema” y “DigitalData”
"""
def obtener_columnas(df):
    details = columna_details(df)
    jobDigital = columna_JobDigital(df)
    print('fin obtener_columnas')
    return details, jobDigital







