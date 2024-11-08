import pandas as pd
from nltk.corpus import stopwords
from nltk import tokenize
from transformaciones.funciones_generales.fun_general import normalize, notnumber
from transformaciones.funciones_generales.fun_aux import obtener_json
import operator
import re

"""
Funciones
"""
"""
Creación de columnas binarias
"""
def get_categorias(words, keywor):
  for keyword in keywor:
    if len(keyword.split()) == 1: # Si es una sola palabra
      if normalize(keyword).lower().endswith("*"):
        x = any([word.startswith(normalize(keyword[:-1])) for word in words.split()])
        if x:
          return "Sí"
      else:
        if normalize(keyword).lower() in words.split():
          return "Sí"
    else: # Si son 2 o mas palabras
      if keyword in words:
        return "Sí"
  return "No"

"""
Identificación de categorias 
"""
def logica_cats(words, diccionario):
    results = dict()
    for cat, keywds in diccionario.items():
        counter = 0
        for keyword in keywds:
          if len(keyword.split()) == 1:
            if normalize(keyword).lower().endswith("*"):
              x = any([word.startswith(normalize(keyword[:-1])) for word in words.split()])
              if x:
                counter += 1
            else:
              if normalize(keyword).lower() in words.split():
                counter += 1
          elif keyword in words:
              counter += 1
        if counter:
            results[cat] = counter
    return results


def set_cats(words, diccionario):
    results = logica_cats(words, diccionario)
    if len(results):
        return max(results.items(), key=operator.itemgetter(1))[0]
    else:
        return "N/A"
    
def set_cats_vacio(words, diccionario):
    results = logica_cats(words, diccionario)
    if len(results):
        return max(results.items(), key=operator.itemgetter(1))[0]
    else:
        return ''
    

patron_universidad = r'universidad\w*'
def set_cats_educacion(words, diccionario):
    results = dict()
    for cat, keywds in diccionario.items():
        counter = 0
        for keyword in keywds:
          if len(keyword.split()) == 1:
            if normalize(keyword).lower().endswith("*"):
              x = any([word.startswith(normalize(keyword[:-1])) for word in words.split()])
              if x:
                counter += 1
            else:
              if normalize(keyword).lower() in words.split():
                counter += 1
          elif keyword in words:
              counter += 1
          # busca si existe la palabra junto con otras palabras (palabras pegadas)
          else:
                coincide = re.search(patron_universidad, words.lower())
                if coincide:
                   counter += 1
                # break
        if counter:
            results[cat] = counter
    if len(results):
        return max(results.items(), key=operator.itemgetter(1))[0]
    else:
        return "N/A"


def set_empresa(words, diccionario):
    results = dict()
    for cat, keywds in diccionario.items():
        counter = 0
        for keyword in keywds:
          if len(keyword.split()) == 1:
            if keyword.endswith("*"):
              x = any([word.startswith(keyword[:-1]) for word in words.split()])
              if x:
                counter += 1
            else:
              if keyword in words.split():
                counter += 1
          elif keyword in words:
              counter += 1
        if counter:
            results[cat] = counter
    if len(results):
        return max(results.items(), key=operator.itemgetter(1))[0]
    else:
        return words


"""Tokenización y remoción de stop words"""
stopw = [w for w in stopwords.words('spanish')]
punc_lit = [u'.', u'[', ']', u',', u';', u'', u')', u'),', u' ', u'(', u':']
stopw.extend(punc_lit)

#Funciones de tokenizacion
def tokenizar_limpiar_titulo(df_original):
    df_copy = df_original.copy()
    df_copy['tokenized_title'] = df_copy['Titulo de puesto'].apply(lambda x:[word for word in tokenize.word_tokenize(x if type(x) == str else "") if word.isalpha() or word.count("/") or word.count("-")])
    df_copy = df_copy[df_copy["tokenized_title"].str.len() != 0]
    df_copy['clean_title'] = df_copy['tokenized_title'].apply(lambda x: [normalize(token).lower() for token in x if normalize(token).lower() not in stopw])
    df_copy["full_clean_title"] = df_copy["clean_title"].apply(lambda x: " ".join(x))
    return df_copy

def tokenizar_limpiar_descripcion(df_original):
    df_copy = df_original.copy()
    df_copy['tokenized_descr'] = df_copy['Descripción del puesto'].apply(lambda x:[word for word in tokenize.word_tokenize(x if type(x) == str else "") if word.isalpha() or word.count("/") or word.count("-")])
    df_copy = df_copy[df_copy["tokenized_descr"].str.len() != 0]
    df_copy['clean_descr'] = df_copy['tokenized_descr'].apply(lambda x: [normalize(token).lower() for token in x if normalize(token).lower() not in stopw])
    df_copy["full_clean_descr"] = df_copy["clean_descr"].apply(lambda x: " ".join(x))
    return df_copy

def tokenizar_limpiar_requisitos(df_original):
  df_copy = df_original.copy()
  df_copy['RS'] = df_copy['Requisitos'].apply(lambda x: notnumber(str(x)))
  df_copy['tokenized_rs'] = df_copy["RS"].apply(lambda x:[word for word in tokenize.word_tokenize(x if type(x) == str else "") if word.isalpha() or word.count("/") or word.count("-")])
  df_copy['clean_rs'] = df_copy['tokenized_rs'].apply(lambda x: [normalize(token).lower() for token in x if normalize(token).lower() not in stopw])
  df_copy["full_clean_rs"] = df_copy["clean_rs"].apply(lambda x: " ".join(x))
  return df_copy

# Realiza todas las tokenizaciones
def tokenizar_conjunto(df):
  df= tokenizar_limpiar_titulo(df)
  df= tokenizar_limpiar_descripcion(df)
  df= tokenizar_limpiar_requisitos(df)
  return df


"""Filtros por plataforma"""

def filtro_compu(df):
  filtro_computrabajo = df['Plataforma'].str.contains('Computrabajo', case=False, na=False)
  return filtro_computrabajo

def filtro_teco(df):
  filtro_tecoloco = df['Plataforma'].str.contains('tecoloco', case=False, na=False)
  return filtro_tecoloco

def modificar_bairesdev(df):
  patron_baires = r"(?:'?)overseeing(?:'?)\s(?:'?)team(?:'?)\s(?:'?)of(?:'?)\s(?:'?)experienced(?:'?)\s(?:'?)front(?:'?)\s(?:'?)and(?:'?)\s(?:'?)back(?:'?)\s(?:'?)|overseeing team of experienced front and back"
  df.loc[(df["Nombre empresa"] == "BairesDev") | (df["Nombre empresa"] == "BAIRESDEV"), "full_clean_descr"] = df["full_clean_descr"].apply(lambda x: re.sub(patron_baires, "", str(x)))
  return df


"""Funciones de transformación"""
def obtener_jornada(df_jornada, filtro_tecoloco, DICCIONARIO):
  # obtener horas de trabajo y si la jornada esta vacia poner tiempo completo
  # Obtener jornada de tipo de contrato en tecoloco
  df_jornada.loc[filtro_tecoloco, 'Jornada'] = df_jornada.loc[filtro_tecoloco, 'Tipo de contrato'].apply(lambda x: set_cats(normalize(x), DICCIONARIO["keywords"]["jornada"]))
  # Borrar horarios de columna tipo de contrato de tecoloco.
  df_jornada.loc[(filtro_tecoloco) & ((df_jornada['Tipo de contrato'] == 'Tiempo completo') | (df_jornada['Tipo de contrato'] == 'Medio tiempo') | (df_jornada['Tipo de contrato'] == 'Horario nocturno')), 'Tipo de contrato'] = ''
  # Obtener jornada de description
  df_jornada.loc[(filtro_tecoloco) & (df_jornada['Jornada'] == 'N/A'), 'Jornada'] = df_jornada.loc[filtro_tecoloco, 'full_clean_descr'].apply(lambda x: set_cats(normalize(x), DICCIONARIO["keywords"]["jornada"]))
  # completar con tiempo completo si es nulo o esta vacio
  df_jornada.loc[df_jornada['Jornada'].isna(), 'Jornada'] = 'Tiempo Completo'
  df_jornada.loc[df_jornada['Jornada'] == "N/A", 'Jornada'] = 'Tiempo Completo'
  return df_jornada

def obtener_modalidad(df_modalidad, filtro_tecoloco, DICCIONARIO):
  # obtener modalidad de los vacios y unificar las categorias hibrido y remoto
  df_modalidad.loc[df_modalidad['Modalidad'].isna(), 'Modalidad'] = df_modalidad.loc[:, 'full_clean_descr'].apply(lambda x: set_cats(normalize(x), DICCIONARIO["keywords"]["modalidad"]))
  df_modalidad.loc[(filtro_tecoloco) & (df_modalidad['Modalidad'] == 'N/A'), 'Modalidad'] = df_modalidad.loc[filtro_tecoloco, 'Tipo de contrato'].apply(lambda x: set_cats(normalize(x), DICCIONARIO["keywords"]["jornada"]))
  df_modalidad.loc[df_modalidad['Modalidad'] == "", 'Modalidad'] = df_modalidad.loc[:, 'full_clean_descr'].apply(lambda x: set_cats(normalize(x), DICCIONARIO["keywords"]["modalidad"]))
  # Borrar remoto de tipo de contrato de tecoloco
  df_modalidad.loc[(filtro_tecoloco) & ((df_modalidad['Tipo de contrato'] == 'Remoto')), 'Tipo de contrato'] = ''
  df_modalidad.loc[df_modalidad['Modalidad'] == 'Presencial y remoto' , 'Modalidad'] = 'Hibrido'
  df_modalidad.loc[df_modalidad['Modalidad'] == 'Virtual' , 'Modalidad'] = 'Remoto'
  return df_modalidad

def obtener_educacion(df_educacion, filtro_computrabajo, DICCIONARIO):
  # Obtiene el valor del Nivel Universitario de requisitos
  df_educacion.loc[filtro_computrabajo, 'RS_Data'] = df_educacion.loc[filtro_computrabajo, 'full_clean_rs'].apply(lambda x: set_cats_educacion(normalize(x), DICCIONARIO["keywords"]["educacion"]) if x is not None or set_cats_vacio(normalize(x), DICCIONARIO["keywords"]["filtro_educacion"]) == '' else '')
  # Completar la columna educacion con los datos de RS_Data
  df_educacion.loc[df_educacion['RS_Data'] != 'N/A', 'Educación'] = df_educacion['RS_Data']
  # # obtener educación
  df_educacion.loc[df_educacion['Educación'] == '', 'Educación'] = df_educacion.loc[df_educacion['Educación'] == '', 'full_clean_descr'].apply(lambda x: set_cats_vacio(normalize(x), DICCIONARIO["keywords"]["educacion"]) if set_cats_vacio(normalize(x), DICCIONARIO["keywords"]["filtro_educacion"]) == '' else '')
  # buscar otro tipo de educación en requisitos y descripcion
  df_educacion.loc[df_educacion['RS_Data'] == 'N/A', 'RS_Data'] = df_educacion.loc[filtro_computrabajo, 'full_clean_rs'].apply(lambda x: set_cats_vacio(normalize(x), DICCIONARIO["keywords"]["filtro_educacion2"]) if x is not None else '')
  df_educacion.loc[df_educacion['RS_Data'] == 'Otro', 'Educación'] = df_educacion['RS_Data']
  df_educacion.loc[df_educacion['Educación'] == '', 'Educación'] = df_educacion.loc[df_educacion['Educación'] == '', 'full_clean_descr'].apply(lambda x: set_cats_vacio(normalize(x), DICCIONARIO["keywords"]["filtro_educacion2"]) if x is not None else '')
  # si los datos estan vacios completa con no piden requisito nivel universitario
  df_educacion.loc[df_educacion['Educación'] == '', 'Educación'] = "Sin datos"
  return df_educacion

def obtener_experiencia(df_experiencia, filtro_computrabajo, DICCIONARIO):
  # obtener la experiencia de requisitos de CompuTrabajo y la agrega como si en requiere experiencia si dice NO
  df_experiencia.loc[filtro_computrabajo, 'RS_Data_Exp'] = df_experiencia.loc[filtro_computrabajo, 'full_clean_rs'].apply(lambda x: set_cats_educacion(x, DICCIONARIO["keywords"]["experiencia"]) if x is not None else None)
  df_experiencia.loc[(df_experiencia['RS_Data_Exp'] == 'requiere experiencia') & (df_experiencia['requiere experiencia'] == 'No'), 'requiere experiencia'] = 'Sí'
  return df_experiencia

def obtener_empresa(df_empresa, DICCIONARIO):
  # obtener nombre de empresa
  df_empresa.loc[:,"Nombre empresa"] = df_empresa.loc[:,"Nombre empresa"].apply(lambda x: set_empresa(x, DICCIONARIO["keywords"]["empresas"]))
  df_empresa = df_empresa.loc[:, ~df_empresa.columns.str.contains('^Unnamed')]
  return df_empresa

def nombres_contratos(df_contratos, DICCIONARIO):
   #  Modifica los nombres en tipo de contratos de acuerdo al diccionario
  df_contratos['Tipo de contrato'] =df_contratos['Tipo de contrato'].apply(lambda x: set_cats_vacio(x, DICCIONARIO["keywords"]["contrato"])if x is not None else x)
  return df_contratos

def transformacion_columnas_binarias(df, DICCIONARIO):
# crear columna para categoria
  df['categoria'] = ''
  # Seccion de tokenizacion de titulo, descripción
  df = tokenizar_conjunto(df)
    # modificar bairesdev
  df = modificar_bairesdev(df)
  # crear 'RS_Data' despues de tokenización
  df['RS_Data'] = ''
  # busca el nombre de la categoria (perfiles) en la descripción
  df['categoria'] = df["full_clean_descr"].apply(lambda x: set_cats(normalize(x).lower(), DICCIONARIO["keywords"]["perfiles"]))
  # obtener binario de cada categoria menos horas de trabajo
  for categoria, keywds in DICCIONARIO["keywords"]["categorias"].items():
    df[categoria] = df["full_clean_descr"].apply(lambda x: get_categorias(x, keywds))
  return df

# """ Seccion para obtener datos y transformar nombres de Experiencia Jornada, Modalidad, Educación y Empresas (Armar funciones mas pequeñas)
def transformacion_categorias(df_conjunto, filtro_tecoloco, filtro_computrabajo, DICCIONARIO):
    df_jornada = obtener_jornada(df_conjunto,filtro_tecoloco, DICCIONARIO)
    df_modalidad = obtener_modalidad(df_jornada, filtro_tecoloco, DICCIONARIO)
    df_educacion = obtener_educacion(df_modalidad, filtro_computrabajo, DICCIONARIO)
    df_experiencia = obtener_experiencia(df_educacion, filtro_computrabajo, DICCIONARIO)
    df_empresa = obtener_empresa(df_experiencia, DICCIONARIO)
    df_completo = nombres_contratos(df_empresa, DICCIONARIO)
    return df_completo


"""Funciones de correción"""

def funcion_filtro(df):
  #  Agrega N/A al campo categoria data science si se cumple la condición
   df.loc[(df["categoria"] == "Data science / analytics") & (df["Industria de la empresa"] == "restaurantes"), "categoria"] =  "N/A"
   df.loc[(df["categoria"] == "Data science / analytics") & (df["Industria de la empresa"] == "operaciones | logística"), "categoria"] =  "N/A"
   df.loc[(df["categoria"] == "Data science / analytics") & (df["Nombre empresa"] == "Corporación BI"), "categoria"] =  "N/A"
   return df

# completa las categorias donde la binaria es si porque las palabras del diccionario en perfiles y categorias son las mismas
def errores_lectura(df):
    df.loc[(df["categoria"] == "N/A") & (df["Desarrollador"] == "Sí"), "categoria"] =  "Desarrollador"
    df.loc[(df["categoria"] == "N/A") & (df["Data science / analytics"] == "Sí"), "categoria"] =  "Data science / analytics"
    df.loc[(df["categoria"] == "N/A") & (df["Diseñador ux/ui"] == "Sí"), "categoria"] =  "Diseñador ux/ui"
    df.loc[(df["categoria"] == "N/A") & (df["otros puestos tech"] == "Sí"), "categoria"] =  "otros puestos tech"
    return df

def rellenar_stack(df):
    # modificacion de categorias back front y fullstack para rellenar
    df.loc[(df["front-end"] == "Sí") & (df["back-end"] == "Sí") & (df["full-stack"] == "No"), "full-stack"] = "Sí"
    df.loc[(df["full-stack"] == "Sí" ) & (df["front-end"] == "No"), "front-end"] = "Sí"
    df.loc[(df["full-stack"] == "Sí" ) & (df["back-end"] == "No"), "back-end"] = "Sí"    
    return df

def tipo_desarrollador(df):
   df.insert(20, "tipo de desarrollador", "")
   df.loc[df["full-stack"] == "Sí", "tipo de desarrollador"] = "full-stack"
   df.loc[(df["tipo de desarrollador"] == "") & (df["front-end"] == "Sí"), "tipo de desarrollador"] = "front-end"
   df.loc[(df["tipo de desarrollador"] == "") & (df["back-end"] == "Sí"), "tipo de desarrollador"] = "back-end"
   df.loc[df["tipo de desarrollador"] == "", "tipo de desarrollador"]   = "N/A"
   return df

patron_menosexperiencia = r"Menos de (\d{1,2})\s*años?\s*(?:de)?\s*experiencia"
patron_experiencia1 = r"(\d+)\s*(?:años?\s*(?:de)?\s*experiencia)?"
numeroexp = r'\d+'
def experiencia(df,filtro_computrab, filtro_tecol, dict):
  #  crea la columna data experiencia
   df.insert(20, "data experiencia", "")
  #  Obtiene la experiencia de requisitos de acuerdo a los patrones
   df["data experiencia"] = df["Requisitos"].apply(lambda x: re.search(patron_menosexperiencia, str(x)).group() if re.search(patron_menosexperiencia, str(x)) else "")
   df.loc[df["data experiencia"] == "", "data experiencia"] = df["Requisitos"].apply(lambda x: re.search(patron_experiencia1, str(x)).group() if re.search(patron_experiencia1, str(x)) else "")
  # Detecta valores numericos solos (errores) y los remplaza por vacio
   df.loc[~df["data experiencia"].apply(lambda x: isinstance(x, str) and any(c.isalpha() for c in x)), "data experiencia"] = ""
   #  crea la columna años de antiguedad
   df.insert(10, "años de antiguedad", "")
  #  Asigna valores de meno de un año a años de antiguedad con menos uno
   df["años de antiguedad"] = df["data experiencia"].apply(lambda x: -1 if re.search(patron_menosexperiencia, str(x)) else "")
  #  Asigna valores de antiguedad en base a data experiencia
   df.loc[df["años de antiguedad"] == "", "años de antiguedad"] = df["data experiencia"].apply(lambda x: int(re.findall(numeroexp, str(x))[0]) if re.findall(numeroexp, str(x)) else "")
  # Experiencia (binaria) para computrabajo
   df.loc[(df["años de antiguedad"] != "") & (df["requiere experiencia"] == "No") & (df["años de antiguedad"] != -1), "requiere experiencia"] = "Sí"
   return df

"""
funcion principal de transformación:
"""
def fun_transformacion_final(df_conjunto):
  """
  Importar
  """
  # importar JSON
  ruta_json = "./diccionario.json"
  DICCIONARIO = obtener_json(ruta_json)

  # Filtros
  filtro_computrabajo = filtro_compu(df_conjunto)
  filtro_tecoloco = filtro_teco(df_conjunto)

  """
    Ejecución
  """
  df_final = transformacion_columnas_binarias(df_conjunto, DICCIONARIO)
  df_final = transformacion_categorias(df_final, filtro_tecoloco, filtro_computrabajo, DICCIONARIO)
  df_final = funcion_filtro(df_final)
  df_final = errores_lectura(df_final)
  df_final = rellenar_stack(df_final)
  df_final = tipo_desarrollador(df_final)
  df_final = experiencia(df_final, filtro_computrabajo, filtro_tecoloco, DICCIONARIO)
  print('fin_transformaciónfinal')
  return df_final




