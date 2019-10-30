import numpy as np
import pandas as pd
from geopy.distance import geodesic


def coord_from_codigo(codigo, municipios):
    '''
    Retorna a latitude e longitude
    '''
    try:
        return municipios.loc[codigo]['LATITUDE'], municipios.loc[codigo]['LONGITUDE']
    except:
        return 0, 0
    
def lat_from_codigo(codigo, municipios):
    '''
    Retorna latitude
    '''
    return coord_from_codigo(codigo, municipios)[0] if coord_from_codigo(codigo, municipios)[0]!=0 else np.nan

def lon_from_codigo(codigo, municipios):
    '''
    Retorna longitude
    '''
    return coord_from_codigo(codigo, municipios)[1] if coord_from_codigo(codigo, municipios)[1]!=0 else np.nan
    
def calculte_distance(row, municipios):
    '''
    Calcula a distância dada as coordenadas
    '''
    try:
        cidade_tratamento = row['AP_UFMUN']
        cidade_paciente = row['AP_MUNPCN']
        lat_cid_trat = municipios['LATITUDE'][str(cidade_tratamento)]
        long_cid_trat = municipios['LONGITUDE'][str(cidade_tratamento)]
        lat_cid_pac = municipios['LATITUDE'][str(cidade_paciente)]
        long_cid_pac =municipios['LONGITUDE'][str(cidade_paciente)]
        return geodesic((lat_cid_pac, long_cid_pac), (lat_cid_trat, long_cid_trat)).km
    except:
        # se o codigo do municipio não existir (e.g. por erro de digitação) então retorna NaN
        return np.nan
    
def generate_df_estado(df, municipios, codigo_uf):
    '''
    Cria um dataframe para um estado especifico
    '''
    bool_index = (df['AP_MUNPCN'].str.startswith(codigo_uf)) & (df['AP_UFMUN'].str.startswith(codigo_uf))
    df_estado = df[bool_index].reset_index()
    
    df_estado['LAT_MUN'] = df_estado.apply(lambda row: municipios.loc[row['AP_UFMUN']]['LATITUDE'], axis=1)
    df_estado['LON_MUN'] = df_estado.apply(lambda row: municipios.loc[row['AP_UFMUN']]['LONGITUDE'], axis=1)
    df_estado['LAT_PCN'] = df_estado.apply(lambda row: municipios.loc[row['AP_MUNPCN']]['LATITUDE'], axis=1)
    df_estado['LON_PCN'] = df_estado.apply(lambda row: municipios.loc[row['AP_MUNPCN']]['LONGITUDE'], axis=1)
    
    return df_estado