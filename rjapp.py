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
        nrows=2721,
    )
    return df

df = busca_df()

# Fim do DF

st.subheader(":bar_chart: DASBOARD DE VENDAS ")

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

    meta = round(tab1_qtde_grupo.loc[:,('Meta')].sum(),2)
    fat_total_vendedor = round(tab1_qtde_grupo.loc[:,('Realizado')].sum(),2)
    percentual = round(fat_total_vendedor / meta * 100, 2)

myBar = st.progress(0)
for num in range(100):
    time.sleep(0.003)
    myBar.progress(num+1)

tab1_qtde_grupo = tab1_qtde_grupo.groupby('Grupo').sum().reset_index()

tab1_qtde_grupo = tab1_qtde_grupo.drop(columns=['Setor', '%.', 'Base Cli.', 'Rota', '1-Realizado', '2-Anterior',
                                                '(1-2) - Diferença', '.%.',
                                                '(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado', '9-Meta',
                                                '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'])
#inserindo a coluna de percentual
tab1_qtde_grupo['Porcentagem: %'] = round(tab1_qtde_grupo['Realizado'] / tab1_qtde_grupo['Meta'] * 100,2 )

col1, col2, col3, col4 = st.columns([1,1,1,1])

with col1:
    st.write('**FATURAMENTO:**')
    st.info(f"R$ {fat_total_vendedor}")

with col2:
    st.write('**PORCENTAGEM:**')
    st.info(f"{percentual} %")

st.markdown("---")

# tab_rota = df.groupby(['Setor', 'Seção', 'Grupo']).sum().reset_index()

# st.bar_chart(tab1_qtde_grupo, x="Meta", y="Realizado")

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

# Criar o gráfico de barras horizontais com cantos superiores direitos arredondados e cor única
grafico_barras = alt.Chart(tab1_qtde_grupo).transform_joinaggregate(
    Meta='sum(Meta)',
    groupby=['Grupo']
).mark_bar(
    cornerRadiusTopRight=10,
    cornerRadiusBottomRight=10,
    color='#3182bd'  # Defina a cor desejada aqui
).encode(
    y=alt.Y('Grupo:N', title='Grupo'),
    x=alt.X('Realizado:Q', title='Realizado'),
    tooltip=['Realizado', 'Meta']
).properties(
    width=600,
    height=400,
    title='Realizado e Meta por Grupo'
)

# Adicionar a linha de meta
linha_meta = alt.Chart(tab1_qtde_grupo).mark_rule(color='red').encode(
    y='Grupo:N',
    x='Meta:Q'
)

# Adicionar textos de Realizado e Meta ao lado de cada barra
text_realizado = grafico_barras.mark_text(
    color='#3366cc',
    align='left',
    baseline='middle',
    dx=9,  # Ajuste a posição horizontal conforme necessário
    dy=-9,  # Ajuste a posição vertical para cima
).encode(
    text='Realizado:Q'
)

text_meta = grafico_barras.mark_text(
    color=' #0000FF',
    align='right',
    baseline='middle',
    dx=-5,  # Ajuste a posição horizontal conforme necessário
    dy=5,   # Ajuste a posição vertical para baixo
).encode(
    text='Meta:Q'
)

# Exibir o gráfico com as legendas e valores ao lado de cada barra
st.altair_chart(grafico_barras + linha_meta + text_realizado + text_meta, use_container_width=True)

