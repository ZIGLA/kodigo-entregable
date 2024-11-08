import os
import pandas as pd
from transformaciones.armadotabla.obtener_columnas import obtener_columnas
from transformaciones.armadotabla.concatenar import concatenar_df
from transformaciones.armadotabla.modificarcol_unioncompu import modificarcol_concatenadocompu
from transformaciones.transformaciontabla.transformacion_final import fun_transformacion_final

if not os.path.exists("../../bbdd"):
    os.mkdir("../../bbdd")

if not os.mkdir("../../bbdd/backup"):
    os.path.exists("../../bbdd/backup")


"""
Preparacion de las tablas y concatenado
"""
# lee la tabla cruda de tecoloco
df = pd.read_excel("bbdd/tecolococrudo.xlsx", index_col=None)
# obtiene las columnas y datos de los diccionarios del scrapping
dfdetails, dfjobposting = obtener_columnas(df)
# Concatena los dos excel generados por obtener columnas
df_tecoloco = concatenar_df(dfdetails, dfjobposting)
# crea, modifica y elimina columnas de tecoloco y luego une el df de tecoloco con computrabajo
df_conjunto = modificarcol_concatenadocompu(df_tecoloco)

"""
Transformaciones
"""
# Transformaciones para obtener las columnas con los datos requeridos
df_ultimo = fun_transformacion_final(df_conjunto)
# Crear el excel de tabla final
df_ultimo.to_excel("tablafinal/tablafinal.xlsx")

