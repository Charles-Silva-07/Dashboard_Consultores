import streamlit as st
import pandas as pd
from PIL import Image
import time

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    layout='wide',
    page_title='DASHBOARD DE VENDAS',
    page_icon='💲',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
    }
)

# --- Criando o dataframe
@st.cache_data
def busca_df():
    df = pd.read_excel(
        io='rjcariri.xlsx',
        index_col=0,
        engine='openpyxl',
        sheet_name='dados',
        usecols='A:AA',
        nrows=2641,
    )
    return df

df = busca_df()

# Dataframe geral
@st.cache_data
def busca_df_volume():
    df_volume = pd.read_excel(
        io='rjcariri.xlsx',
        index_col=0,
        engine='openpyxl',
        sheet_name='volume',
        usecols='A:AA',
        nrows=2641,
    )
    return df_volume

st.subheader(":bar_chart: DASHBOARD DE VENDAS ")

st.subheader("Vendas por volume")

area_dataframe_volume = busca_df_volume()

# Removendo a coluna
area_dataframe_volume['Rota'] = area_dataframe_volume['Rota'] // 100 * 100

# Dataframe removendo as colunas
area_dataframe_volume = area_dataframe_volume.drop(
    columns=['Setor', 'Par/Impar', 'Fornecedor', 'Base Cli.', '1-Realizado',
             '2-Anterior', '(1-2) - Diferença', '.%.', 'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado',
             '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
             ])

with st.sidebar:
    logo_teste = Image.open('logo.png')
    st.image(logo_teste, width=250)
    st.subheader('DASHBOARD COMERCIAL')

    # Utilizando a função unique() para obter valores únicos
    area_options = area_dataframe_volume['Área'].unique()
    area = st.selectbox("Área:", options=sorted(area_options), index=None)

    # Utilizando a função unique() para obter valores únicos rotas centencas mostradas na tela
    rota_area_options = area_dataframe_volume['Rota'].unique()
    rota_area = st.selectbox("Rota Área:", options=sorted(rota_area_options), index=None)

    # Utilizando a função unique() para obter valores únicos das seções
    secao_options = area_dataframe_volume['Seção'].unique()
    secao = st.selectbox("Seção:", options=sorted(secao_options), index=None)

    # Spiner
    with st.spinner("Carregando..."):
        time.sleep(2)
    st.success("Pronto")

# Barra de progresso
myBar = st.progress(0)
for num in range(100):
    time.sleep(0.003)
    progress_value = round((num + 1) / 100, 2)  # Arredonda para duas casas decimais
    myBar.progress(progress_value)

# Destacar coluna com zeros
    def highlight_zeros(value):
        return 'background-color: Red; color: White' if value == 0 else ''

import streamlit as st
import pandas as pd


def highlight_zeros(value):
    return 'background-color: Red' if value == 0 else ''


if area and not (rota_area or secao or (rota_area and secao)):
    area_dataframe_filtered = area_dataframe_volume[area_dataframe_volume['Área'] == area]

    # Agrupar DataFrame
    grouped_df = area_dataframe_filtered.groupby(['Área', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df['Diferença'] = (grouped_df['Realizado'] - grouped_df['Meta']).round(2)

    # Adicionar a coluna 'Percentual %'
    grouped_df['Percentual %'] = ((grouped_df['Realizado'] / grouped_df['Meta']) * 100).round(2)

    # Criar DataFrame com as estilizações
    styled_df = (
        grouped_df.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Percentual %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela
    st.table(styled_df)

# Verificar se 'area' e 'rota_area' são verdadeiros e 'secao' é falso
elif area and rota_area and not secao:
    # Filtrar DataFrame pela área e rota
    area_rota_dataframe_filtered = area_dataframe_volume[
        (area_dataframe_volume['Área'] == area) & (area_dataframe_volume['Rota'] == rota_area)]

    if not area_rota_dataframe_filtered.empty:
        # Agrupar DataFrame filtrado
        grouped_df_area_rota = area_rota_dataframe_filtered.groupby(['Área', 'Rota', 'Grupo']).agg({
            'Realizado': 'sum',
            'Meta': 'sum'
        }).reset_index()

        # Adicionar a coluna 'Diferença'
        grouped_df_area_rota['Diferença'] = (grouped_df_area_rota['Realizado'] - grouped_df_area_rota['Meta']).round(2)

        # Adicionar a coluna 'Percentual'
        grouped_df_area_rota['Percentual %'] = ((grouped_df_area_rota['Realizado'] / grouped_df_area_rota['Meta']) * 100).round(2)

        # Criar DataFrame com as estilizações
        styled_df_area_rota = (
            grouped_df_area_rota.style
                .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
                .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Percentual %': '{:.2f}'})
                .hide_index()
        )

        # Exibir a tabela
        st.table(styled_df_area_rota)
    else:
        st.warning("Não há dados disponíveis para a combinação de Área e Rota selecionadas.")

# Verificar se 'area', 'secao' e 'rota_area' são verdadeiros
elif area and secao and rota_area:
    # Filtrar DataFrame pela área, rota e seção
    area_rota_secao_dataframe_filtered = area_dataframe_volume[
        (area_dataframe_volume['Área'] == area) & (area_dataframe_volume['Rota'] == rota_area) & (area_dataframe_volume['Seção'] == secao)]

    # Agrupar DataFrame filtrado
    grouped_df_area_rota_secao = area_rota_secao_dataframe_filtered.groupby(['Rota', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df_area_rota_secao['Diferença'] = (grouped_df_area_rota_secao['Realizado']-grouped_df_area_rota_secao['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_df_area_rota_secao['Percentual %'] = (
            (grouped_df_area_rota_secao['Realizado'] / grouped_df_area_rota_secao['Meta']) * 100).round(2)

    # Criar DataFrame com as estilizações
    styled_df_area_rota_secao = (
        grouped_df_area_rota_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Percentual %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela estilizada
    st.table(styled_df_area_rota_secao)

# Verificar se 'area', 'secao' e 'rota_area' são verdadeiros
elif area and secao and not rota_area:
    # Filtrar DataFrame pela área e seção
    area_secao_dataframe_filtered = area_dataframe_volume[
        (area_dataframe_volume['Área'] == area) & (area_dataframe_volume['Seção'] == secao)]

    # Remover a coluna 'Rota' do DataFrame filtrado
    area_secao_dataframe_volume_area_secao = area_secao_dataframe_filtered.drop(columns=['Rota'])

    # Agrupar DataFrame filtrado
    grouped_df_area_secao = area_secao_dataframe_volume_area_secao.groupby(['Área', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df_area_secao['Diferença'] = (grouped_df_area_secao['Realizado'] - grouped_df_area_secao['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_df_area_secao['Percentual %'] = ((grouped_df_area_secao['Realizado'] / grouped_df_area_secao['Meta']) * 100).round(2)

    # Criar DataFrame com as estilizações
    styled_df_area_secao = (
        grouped_df_area_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}',  'Percentual %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela estilizada
    st.table(styled_df_area_secao)
