import pandas as pd

"Modificacion de columnas de Tecoloco y concatenacion con compuTrabajo"

columnas = ['Plataforma','Nombre empresa','Descripción de la empresa','Industria de la empresa','Fecha publicación','Link a la búsqueda','Titulo de puesto','Descripción del puesto','Requisitos','Experiencia','Modalidad','Jornada','Salario','Palabras clave','País','Localidad','Provincia','Educación',"Tipo de contrato"]

# Modifica las columnas de acuerdo a un listado: cambio de nombre, creacion de columnas nuevas, filtrado de columnas y ordenado
def modificar_columnastecoloco(df_tecoloco):
    df_tecoloco["joblocation - address - addressCountry"] = df_tecoloco.apply(lambda x: x["País"] if pd.isnull(x["joblocation - address - addressCountry"]) else x["joblocation - address - addressCountry"], axis=1)
    df_tecoloco.drop(columns=["País"], inplace=True)
    df_tecoloco = df_tecoloco.rename({"job__company_name":"Nombre empresa", "job__primary_category_name":"Industria de la empresa", "job__published_date":"Fecha publicación", "url":"Link a la búsqueda", "job__title":"Titulo de puesto", "description":"Descripción del puesto", "job__salary_range":"Salario",  "joblocation - address - addressCountry":"País", "joblocation - address - addressLocality":"Localidad", "Tipo de Contratación":"Tipo de contrato"}, axis=1)
    df_tecoloco["Plataforma"] = "Tecoloco"
    df_tecoloco["Descripción de la empresa"] = ""
    df_tecoloco["Requisitos"] = ""
    df_tecoloco["Experiencia"] = ""
    df_tecoloco["Modalidad"] = ""
    df_tecoloco["Jornada"] = ""
    df_tecoloco["Palabras clave"] = ""
    df_tecoloco["Provincia"] = ""
    df_tecoloco["Educación"] = ""
    df_tecoloco= df_tecoloco.filter(items=columnas ,axis=1)
    df_tecoloco = df_tecoloco[columnas]
    return df_tecoloco

def modificarcol_concatenadocompu(df):
    df_tecoloco = modificar_columnastecoloco(df)
    df_compu = pd.read_excel("bbdd/compucrudo.xlsx")
    df_compu = df_compu[columnas]
    # union df 
    df_unido = pd.concat([df_tecoloco, df_compu], ignore_index=True)
    print('fin modificarcol_concatenadocompu')
    return df_unido