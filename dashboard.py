import os
import pandas as pd
import geopandas as gpd
import streamlit as st
import plotly.express as px

# 1. Caminho do arquivo
base_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(base_dir, 'artifacts', 'shp', 'br_gdf.shp')

# 2. Carregar os dados
print('Carregando dados...')
df = gpd.read_file(path)

# 2. Configurar o título do dashboard
st.title("Dashboard de Setores Censitários")

# 3. Filtros interativos
regiao = st.selectbox("Selecione uma Cidade:", df['NM_MUNIC'].unique())
filtro_df = df[df['NM_MUNIC'] == regiao]

# 4. Criar gráficos
fig = px.bar(filtro_df, x='Cod_setor', y='populacao',
             title=f"População por Setor em {regiao}")
st.plotly_chart(fig)

fig2 = px.scatter(filtro_df, x='densidade',
                  y='renda_dom',
                  title=f"Renda x Densidade em {regiao}")
st.plotly_chart(fig2)

# 5. Resumo
st.write("Resumo dos dados filtrados:")
st.dataframe(filtro_df)
