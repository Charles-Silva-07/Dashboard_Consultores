import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title='DASHBOARD DE VENDAS',
    page_icon='💲',
    layout='wide',
    initial_sidebar_state='expanded',
    menu_items={
        'Get Help': 'http://www.meusite.com.br',
        'Report a bug': "http://www.meuoutrosite.com.br",
        'About': "Esse app foi desenvolvido no nosso Curso."
    }
)

# --- Criar o dataframe

df = pd.read_excel(
    io = 'rjcariri.xlsx',
    engine='openpyxl',
    sheet_name='dados',
    usecols='A:AZ',
    nrows=332,
)

# --- Criar o sidebar
with st.sidebar:
    logo_teste = Image.open('logo.png')
    st.image(logo_teste, width=250)
    st.subheader('MENU - DASHBOOARD DE VENDAS')
    # --- variaveis que vão armazenar os filtors ---#
    fMes = st.selectbox(
        "Selecione o Mês:",
        options=df['Mês'].unique() # options somente valores unicos quando se repetem
    )

    # --- variável produto ---
    fGrupo = st.selectbox(
        "Selecione o Grupo:",
        options=df['Grupo'].unique()
    )
