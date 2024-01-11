import locale
import streamlit as st
import time
import pandas as pd
import altair as alt
from PIL import Image

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

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
        nrows=2773,
    )
    return df


df = busca_df()

# Fim do df faturamento

@st.cache_data
def busca_df_volume():
    df = pd.read_excel(
        io='rjcariri.xlsx',
        index_col=0,
        engine='openpyxl',
        sheet_name='volume',
        usecols='A:AA',
        nrows=2773,
    )
    return df


dataframe_volume = busca_df_volume()

st.subheader(":bar_chart: DASHBOARD DE VENDAS ")

# --- Criar o sidebar
with st.sidebar:
    logo_teste = Image.open('logo.png')
    st.image(logo_teste, width=250)
    st.subheader('DASHBOOARD COMERCIAL')

    # --- variáveis que vão armazenar os filtros
    fSetor = st.selectbox(
        "Setor:",
        options=pd.concat([df['Setor'], dataframe_volume['Setor']]).unique(), index=None
    )

    fSecao = st.selectbox(
        "Seção:",
        options=pd.concat([df['Seção'], dataframe_volume['Seção']]).unique(), index=None
    )

    tab1_qtde_grupo = df.loc[(df['Setor'] == fSetor) & (df['Seção'] == fSecao)]

    with st.spinner("Carregando..."):
        time.sleep(2)
    st.success("Pronto")

    # Arredondar valores
    locale.setlocale(locale.LC_MONETARY, 'pt_BR')
    meta = locale.currency(round(tab1_qtde_grupo['Meta'].sum(), 2), grouping=True)
    fat_total_vendedor = locale.currency(round(tab1_qtde_grupo['Realizado'].sum(), 2), grouping=True)
    percentual = round(tab1_qtde_grupo['Realizado'].sum() / tab1_qtde_grupo['Meta'].sum() * 100, 2)

myBar = st.progress(0)
for num in range(100):
    time.sleep(0.003)
    progress_value = round((num + 1) / 100, 2)  # Arredonda para duas casas decimais
    myBar.progress(progress_value)

tab1_qtde_grupo = tab1_qtde_grupo.groupby('Grupo').sum().reset_index()

# Remover colunas desnecessárias
colunas_para_remover = [
    'Setor', '%.', 'Base Cli.', 'Rota', '1-Realizado', '2-Anterior',
    '(1-2) - Diferença', '.%.', '(4-5) Diferença', 'ST', 'SM', 'Tend. %',
    '8-Realizado', '9-Meta', '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'
]

tab1_qtde_grupo = tab1_qtde_grupo.drop(columns=colunas_para_remover)

# Inserir a coluna de percentual
tab1_qtde_grupo['Porcentagem: %'] = round(tab1_qtde_grupo['Realizado'] / tab1_qtde_grupo['Meta'] * 100, 2)

# Inserir a coluna de diferença
falta_faturamento = tab1_qtde_grupo['Falta'] = round(tab1_qtde_grupo['Realizado'] - tab1_qtde_grupo['Meta'],2)

# Exibindo valor de Faturamento e Percentual no topo
col1, col2, = st.columns([1, 1])

with col1:
    st.write('**FATURAMENTO:**')
    st.info(fat_total_vendedor)

with col2:
    st.write('**PORCENTAGEM:**')
    st.info(f"{percentual} %")

st.markdown("---")
# Fim da Exibição

# Largura do container
st.dataframe(tab1_qtde_grupo, use_container_width=True, hide_index=True)

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
    title='Realizado e Meta por Grupo Faturamento'
)

# Adicionar a linha de meta
linha_meta = alt.Chart(tab1_qtde_grupo).mark_rule(color='red').encode(
    y='Grupo:N',
    x='Meta:Q'
)

# Adicionar textos de Realizado e Meta ao lado de cada barra
text_realizado = grafico_barras.mark_text(
    color='#0886ff',
    fontSize=15,
    align='left',
    baseline='middle',
    dx=9,  # Ajuste a posição horizontal conforme necessário
    dy=-9,  # Ajuste a posição vertical para cima
).encode(
    text='Realizado:Q'
)

text_meta = grafico_barras.mark_text(
    color=' #fffbf4',
    fontSize=15,
    align='right',
    baseline='middle',
    dx=-2,  # Ajuste a posição horizontal conforme necessário
    dy=9,  # Ajuste a posição vertical para baixo
).encode(
    text='Meta:Q'
)

# Adicionar porcentagem de realização da meta ao lado de cada barra
diferenca = grafico_barras.mark_text(
    color='#0886ff',
    fontSize=15,
    align='right',
    baseline='middle',
    dx=150,
    dy= -9,
).encode(
    text='Falta'  # 'O' representa que é um campo ordinal (string)
)

# Exibir o gráfico com as legendas e valores ao lado de cada barra
st.altair_chart(grafico_barras + linha_meta + text_realizado + text_meta + diferenca, use_container_width=True)

# linha abaixo grafico faturamento
st.markdown("---")

# VOLUME
# INICIANDO O VOLUME
# Remover colunas do DataFrame
colunas_para_remover_do_volume = ['Seção', 'Rota', 'Área', 'Setor', 'Par/Impar', 'Fornecedor',
                                  'Base Cli.', '1-Realizado', '2-Anterior', '(1-2) - Diferença', '.%.',
                                  'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado', '9-Meta',
                                  '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %'
                                  ]

tabela_1_de_volume_grupo = dataframe_volume.loc[
(dataframe_volume['Setor'] == fSetor) & (dataframe_volume['Seção'] == fSecao)]
tabela_1_de_volume_grupo = tabela_1_de_volume_grupo.drop(columns=colunas_para_remover_do_volume)
tabela_1_de_volume_grupo = tabela_1_de_volume_grupo.groupby('Grupo').sum().reset_index()
tabela_1_de_volume_grupo['Porcentagem: %'] = round(
tabela_1_de_volume_grupo['Realizado'] / tabela_1_de_volume_grupo['Meta'] * 100, 2)
grupo_volume_falta = tabela_1_de_volume_grupo['Falta'] =round(tabela_1_de_volume_grupo['Realizado'] - tabela_1_de_volume_grupo['Meta'],2)

meta_volume = round(tabela_1_de_volume_grupo['Meta'].sum(), 2)
volume_vendedor = round(tabela_1_de_volume_grupo['Realizado'].sum(), 2)
percentual_volume = round(tabela_1_de_volume_grupo['Realizado'].sum() / tabela_1_de_volume_grupo['Meta'].sum() * 100, 2)

falta_volume = tabela_1_de_volume_grupo['Falta'] = round(tabela_1_de_volume_grupo['Realizado'] - tabela_1_de_volume_grupo['Meta'], 2)


col1, col2, = st.columns([1, 1])

with col1:
    st.write('**VOLUME:**')
    st.info(volume_vendedor)

with col2:
    st.write('**PORCENTAGEM:**')
    st.info(f"{percentual_volume}%")

st.markdown("---")

# Exibir a tabela
st.dataframe(tabela_1_de_volume_grupo, use_container_width=True, hide_index=True)

st.markdown("---")

### GRÁFICOS ###

grafico_barras_volume = alt.Chart(tabela_1_de_volume_grupo).transform_joinaggregate(
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
    title='Realizado e Meta por Grupo - Volume'
)

# Adicionar a linha de meta para o volume
linha_meta_volume = alt.Chart(tabela_1_de_volume_grupo).mark_rule(color='red').encode(
    y='Grupo:N',
    x='Meta:Q'
)

# Adicionar textos de Realizado e Meta ao lado de cada barra para o volume
text_realizado_volume = grafico_barras_volume.mark_text(
    color='#0886ff',
    fontSize=15,
    align='left',
    baseline='middle',
    dx=9,
    dy=-9,
).encode(
    text='Realizado:Q'
)

text_meta_volume = grafico_barras_volume.mark_text(
    color=' #fffbf4',
    fontSize=15,
    align='right',
    baseline='middle',
    dx=-2,
    dy=9,
).encode(
    text='Meta:Q'
)

# exibir falta_volume
falta_volume = grafico_barras_volume.mark_text(
    color='#0886ff',
    fontSize=15,
    align='right',
    baseline='middle',
    dx=150,
    dy=-9
).encode(
    text='Falta'
)

# Exibir o gráfico com as legendas e valores ao lado de cada barra para o volume
st.altair_chart(grafico_barras_volume + linha_meta_volume + text_realizado_volume + text_meta_volume + falta_volume,
                use_container_width=True)

st.markdown("---")

# Define a formatação para a moeda brasileira (BRL)
locale.setlocale(locale.LC_MONETARY, 'pt_BR')

# Obtendo o setor selecionado no Selectbox
setor_selecionado = fSetor

# Filtrando o DataFrame para o setor selecionado e obtendo a soma da coluna 'Realizado'
soma_realizado = df.loc[df['Setor'] == setor_selecionado, 'Realizado'].sum()

# somando a meta do setor selecionado
meta_de_faturamento_setor = df.loc[df['Setor'] == setor_selecionado, 'Meta'].sum()

# inserindo o formato real brasileiro
meta_formatada = locale.currency(meta_de_faturamento_setor, grouping=True)

# calculando a porcentagem da meta
porcentagem_meta_setor = round(soma_realizado / meta_de_faturamento_setor * 100, 2)

# Formatando a soma como moeda brasileira (BRL)
soma_formatada = locale.currency(soma_realizado, grouping=True)

# Realizando a subtração do realizado menos a meta para trazer a diferença
falta_fat = meta_de_faturamento_setor =round(soma_realizado - meta_de_faturamento_setor, 2)

# Formatando a soma como moeda brasileira (BRL)
falta_faturamento_formatada = locale.currency(falta_fat, grouping=True)

# Exibindo os resultados
col1, col2, col3, col4, = st.columns([1, 1, 1, 1])

with col1:
    st.write(f'**FATURAMENTO SETOR: {setor_selecionado}**')
    st.info(soma_formatada)

with col2:
    st.write('**META FATURAMENTO:**')
    st.info(meta_formatada)

with col3:
    st.write('**FALTA:**')
    st.info(falta_faturamento_formatada)  #falta

with col4:
    st.write('**PORCENTAGEM META:**')
    st.info(f"{porcentagem_meta_setor}%")

# EXIBIR FATURAMENTO POR ROTAS
mostrar_por_rotas = on = st.toggle('Exibir Faturamento')
if on:
    tab_rota = df.loc[(df['Setor'] == fSetor) & (df['Grupo'])]
    tab_rota['%'] = round(tab_rota['Realizado'] / tab_rota['Meta'].sum() * 100, 2)
    colunas_rota_para_remover = [
        'Seção', 'Par/Impar', 'Fornecedor', '%.', 'Base Cli.', '1-Realizado', '2-Anterior',
        '(1-2) - Diferença', '.%.', '(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado',
        '9-Meta', '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'
    ]
    tab_rota = tab_rota.drop(columns=colunas_rota_para_remover)

    # Ordenando as colunas do DataFrame tab_rota
    tab_rota = tab_rota[['Área', 'Setor', 'Rota', 'Grupo', 'Realizado', 'Meta', '%']]

    # Classificar as rotas do menor para o maior
    tab_rota = tab_rota.sort_values(by=['Grupo', 'Rota'])
    falta_grup_fat = tab_rota['Falta'] = round(tab_rota['Realizado'] - tab_rota['Meta'], 2)


    # Largura do container
    st.dataframe(tab_rota, use_container_width=True, hide_index=True)

# Fim mostrar por rotas

st.markdown("---")
### INICIO DE MOSTRAR VOLUME POR ROTAS

# # mostrar por rotas para o volume
mostrar_por_rotas_volume = on = st.toggle('Exibir Volume')
if on:
    tab_rota_volume = dataframe_volume.loc[(dataframe_volume['Setor'] == fSetor) & (dataframe_volume['Grupo'])]
    tab_rota_volume['%'] = round(tab_rota_volume['Realizado'] / tab_rota_volume['Meta'].sum() * 100, 2)
    colunas_rota_para_remover_volume = [
        'Seção', 'Par/Impar', 'Fornecedor', '%.', 'Base Cli.', '1-Realizado', '2-Anterior',
        '(1-2) - Diferença', '.%.', '(4-5) Diferença', 'ST', 'SM', 'Tend. %', '8-Realizado',
        '9-Meta', '(8-9) Diferença', '.%', 'branco', 'branco1', 'branco2'
    ]
    tab_rota_volume = tab_rota_volume.drop(columns=colunas_rota_para_remover_volume)

    # Ordenando as colunas do DataFrame tab_rota_volume
    tab_rota_volume = tab_rota_volume[['Área', 'Setor', 'Rota', 'Grupo', 'Realizado', 'Meta', '%']]

    # Classificar as rotas do menor para o maior
    tab_rota_volume = tab_rota_volume.sort_values(by=['Grupo', 'Rota'])
    falta_grup_vol = tab_rota_volume['Falta'] = round(tab_rota_volume['Realizado'] - tab_rota_volume['Meta'], 2)

    # Largura do container
    st.dataframe(tab_rota_volume, use_container_width=True, hide_index=True)

# Fim mostrar por rotas para o volume
### FIM VOLUME POR ROTAS
