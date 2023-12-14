import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


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
    st.subheader('DASHBOOARD COMERCIAL')

    # --- variaveis que vão armazenar os filtors
    fSetor = st.selectbox(
        "setor:",
        options=df['Setor'].unique(), index=None
    )

    fSecao = st.selectbox(
        "seção:",
        options=df['Seção'].unique(), index=None
    )

    tab1_qtde_grupo = df.loc[(
        df['Setor'] == fSetor) &
        (df['Seção'] == fSecao)
    ]

st.write('Faturamento')
tab1_qtde_grupo = tab1_qtde_grupo.groupby('Grupo').sum().reset_index()

tab1_qtde_grupo = tab1_qtde_grupo.drop(columns=['%.','Setor', 'Base Cli.', 'Rota', '1-Realizado', '2-Anterior', '(1-2) - Diferença', '.%.',
'(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado','9-Meta', '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'])

# Remove os indices no inicio do df
st.dataframe(tab1_qtde_grupo, hide_index=True)