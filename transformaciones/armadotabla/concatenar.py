import pandas as pd
# Concatena los data frames de tecoloco
def concatenar_df(df_details, df_job):
    df_details = df_details.rename({"url":"url2"}, axis=1)
    df_final = pd.concat([df_details, df_job], axis=1)
    df_final.reset_index
    df_final = df_final.loc[:, ~df_final.columns.str.contains('^Unnamed')]
    print('fin_concatenar')
    return df_final