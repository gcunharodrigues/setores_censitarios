import os
import pandas as pd
import numpy as np
import geopandas as gpd
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium


@st.cache_data
def load_data(file_path):
    """Load data from a CSV file."""
    print('Carregando dados...')
    return pd.read_csv(file_path, encoding='utf-8')


@st.cache_data
def load_geodata(file_path):
    """Load geodata from a parquet file."""
    print('Carregando geodados...')
    return gpd.read_parquet(file_path)


def main():
    """Criação de dashboard que filtra pelos municípios do Brasil os setores 
    censitários com renda domiciliar e densidade populacional conforme 
    desejado."""
    # 1. Define the file path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, 'artifacts', 'br_data.csv')

    # 2. Load the data
    df = load_data(path)
    df['Cod_setor'] = df['Cod_setor'].astype(str)

    # 2. Load the geodata
    geodata_path = os.path.join(base_dir, 'artifacts', 'br_geo_gdf.parquet')
    geodata = load_geodata(geodata_path)
    geodata['Cod_setor'] = geodata['Cod_setor'].astype(str)

    # 3. Set the dashboard title
    st.title("Dashboard de Setores Censitários")
    st.sidebar.title("Escolha os filtros:")
    st.write("")

    # 4. Interactive filters
    regiao = st.sidebar.multiselect("Selecione as cidades:",
                                    df['Nome_do_municipio'].unique(), default="SÃO PAULO")
    renda_min = st.sidebar.number_input('Renda mínima',
                                        min_value=df['renda_dom'].min(),
                                        max_value=df['renda_dom'].max(),
                                        value=4500.0)
    densidade_min = st.sidebar.number_input('Densidade mínima',
                                            min_value=df['densidade'].min(),
                                            max_value=df['densidade'].max(),
                                            value=150.0)
    filtro_df = df[(df['Nome_do_municipio'].isin(regiao)) &
                   (df['renda_dom'] >= renda_min) &
                   (df['densidade'] >= densidade_min)]
    filtro_df = pd.merge(filtro_df, geodata, on='Cod_setor')

    # 5. Create map
    setores_gdf = gpd.GeoDataFrame(filtro_df, geometry='geometry')

    map = folium.Map(location=[-23.5633, -46.66744],
                     tiles='Cartodb Positron',
                     zoom_start=10)
    borders_style = {
        'color': 'green',
        'weight': 0,
        'fillColor': 'green',
        'fillOpacity': 0.3,
    }
    setores = folium.GeoJson(data=setores_gdf,
                             style_function=lambda x: borders_style,
                             )
    setores.add_to(map)

    out = st_folium(map, width=1280, height=720, returned_objects=[])

    # 6. Create scatter plot
    regiao_list = ', '.join(regiao[:-1]) + ' e ' + regiao[-1]\
        if len(regiao) > 1 else ', '.join(regiao)
    fig1 = px.scatter(filtro_df, x='densidade', y='renda_dom',
                      title=f"Renda x Densidade em {regiao_list}")
    st.plotly_chart(fig1)


if __name__ == "__main__":
    main()
