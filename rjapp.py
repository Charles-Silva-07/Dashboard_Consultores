import time

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

@st.cache_data
def busca_df():
    df = pd.read_excel(
        io = 'rjcariri.xlsx', index_col=0,
        engine='openpyxl',
        sheet_name='dados',
        usecols='A:AA',
        nrows=2221,
    )
    return df

df = busca_df()

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
    with st.spinner("Carregando..."):
        time.sleep(2)
    st.success("Pronto")

myBar = st.progress(0)
for num in range(100):
    time.sleep(0.003)
    myBar.progress(num+1)

st.write('Meta Faturamento')
tab1_qtde_grupo = tab1_qtde_grupo.groupby('Grupo').sum().reset_index()

tab1_qtde_grupo = tab1_qtde_grupo.drop(columns=['Setor', '%.', 'Base Cli.', 'Rota', '1-Realizado', '2-Anterior',
                                                '(1-2) - Diferença', '.%.',
                                                '(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado', '9-Meta',
                                                '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'])

#inserindo a coluna de percentual

tab1_qtde_grupo['%'] = round(tab1_qtde_grupo['Realizado'] / tab1_qtde_grupo['Meta'].sum()*100, 2 )

# Remove os indices no inicio do df
st.dataframe(tab1_qtde_grupo, use_container_width=True, hide_index=True)

mostrar_por_rotas = \
    on = st.toggle('Exibir por rotas')
if on:
    tab_rota = df.loc[(df['Setor'] == fSetor) & (df['Grupo'])]
    tab_rota['%'] = round(tab_rota['Realizado'] / tab_rota['Meta'].sum()*100, 2 )
    tab_rota = tab_rota.drop(columns=['Seção', 'Par/Impar', 'Fornecedor', '%.', 'Base Cli.', '1-Realizado', '2-Anterior',
                                      '(1-2) - Diferença', '.%.', '(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado',
                                      '9-Meta', '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'])

    # ordenando as colunas do meu df tab_rota
    tab_rota = tab_rota[['Área', 'Setor', 'Rota', 'Grupo', 'Realizado', 'Meta', '%']]

    #Largura do container
    st.dataframe(tab_rota, use_container_width=True, hide_index=True)

# tab_rota = df.groupby(['Setor', 'Seção', 'Grupo']).sum().reset_index()

# st.bar_chart(tab1_qtde_grupo, x="Meta", y="Realizado")
