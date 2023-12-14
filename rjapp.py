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
    io = 'rjcariri.xlsx', index_col=0,
    engine='openpyxl',
    sheet_name='dados',
    usecols='A:AA',
    nrows=2221,
)

# --- Criar o sidebar
with st.sidebar:
    logo_teste = Image.open('logo.png')
    st.image(logo_teste, width=250)
    st.subheader('MENU - DASHBOOARD CONSULTORES')

    # --- variaveis que vão armazenar os filtors
    fSetor = st.selectbox(
        "Selecione o Setor:",
        options=df['Setor'].unique()
    )

    fSecao = st.selectbox(
        "Selecione o Seçao:",
        options=df['Seção'].unique()
    )

    tab1_qtde_grupo = df.loc[(
        df['Setor'] == fSetor) &
        (df['Seção'] == fSecao)
    ]

st.write('Faturamento')
tab1_qtde_grupo = tab1_qtde_grupo.groupby('Grupo').sum().reset_index()

tab1_qtde_grupo = tab1_qtde_grupo.drop(columns=['Setor', 'Base Cli.', 'Rota', '1-Realizado', '2-Anterior', '(1-2) - Diferença', '.%.',
'(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado','9-Meta', '(8-9) Diferença', '.%'])

tab1_qtde_grupo.drop(['branco','branco1','branco2'], axis=1, inplace=True)

tab1_qtde_grupo
