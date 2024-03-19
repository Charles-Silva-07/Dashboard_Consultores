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

with open("style.css") as f:
    # Adicione um bloco de código CSS para personalizar o estilo
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Criando o dataframe
@st.cache_data
def busca_df_faturamento():
    df_fat = pd.read_excel(
        io='rjcariri.xlsx',
        index_col=0,
        engine='openpyxl',
        sheet_name='dados',
        usecols='A:AA',
        nrows=5561,
    )
    return df_fat


# def imagem_fundo():
#     # Carrega a imagem do seu diretório local
#     image = open('logo.png', 'rb')
#     image_bytes = image.read()
#
#     # Exibe a imagem na página do Streamlit
#     st.image(image_bytes, use_column_width=True)


# Carregando a imagem
background_image = "logo.png"
st.image(background_image, use_column_width=True)



# Dataframe geral
@st.cache_data
def busca_df_volume():
    df_volume = pd.read_excel(
        io='rjcariri.xlsx',
        index_col=0,
        engine='openpyxl',
        sheet_name='volume',
        usecols='A:AA',
        nrows=5561,
    )
    return df_volume


st.subheader(":bar_chart: DASHBOARD DE VENDAS")

# st.subheader("Vendas por volume")

#DataFrame para as Regionail Volume
df_regional = busca_df_volume()
df_regional = df_regional.reset_index()

df_regional = df_regional.drop(
    columns=['Setor', 'Par/Impar', 'Fornecedor', 'Base Cli.', '1-Realizado',
             '2-Anterior', '(1-2) - Diferença', '.%.', 'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado',
             '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
             ])

#DataFrame para as Regionail Faturamento
df_regional_fat = busca_df_faturamento()
df_regional_fat = df_regional_fat.reset_index()

df_regional_fat = df_regional_fat.drop(
    columns=['Setor', 'Par/Impar', 'Fornecedor', 'Base Cli.', '1-Realizado',
             '2-Anterior', '(1-2) - Diferença', '.%.', 'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado',
             '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
             ])



# DataFrame para as areas
area_dataframe_volume = busca_df_volume()

# DataFrame para os SETORES
dataframe_volume = busca_df_volume()

# Removendo as colunas do dataframe_volume não necessarioas
dataframe_volume = dataframe_volume.drop(columns=['Par/Impar', 'Fornecedor','Base Cli.', '1-Realizado', '2-Anterior', '(1-2) - Diferença', '.%.', 'branco'
                        ,'(4-5) Diferença', '%.',
                        'branco1', '8-Realizado', '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
])

# Removendo a coluna
area_dataframe_volume['Rota'] = area_dataframe_volume['Rota'] // 100 * 100

# Dataframe removendo as colunas
area_dataframe_volume = area_dataframe_volume.drop(
    columns=['Setor', 'Par/Impar', 'Fornecedor', 'Base Cli.', '1-Realizado',
             '2-Anterior', '(1-2) - Diferença', '.%.', 'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado',
             '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
             ])
# Adicionando porcentagem aos setores
dataframe_volume['Perc. %'] = round(dataframe_volume['Realizado'] / dataframe_volume['Meta'] * 100, 1)

dataframe_volume['Diferença'] = (dataframe_volume['Realizado'] - dataframe_volume['Meta']).round(2)

with st.sidebar:
    logo_teste = Image.open('logo.png')
    st.image(logo_teste, width=250)
    st.subheader('DASHBOARD COMERCIAL')


    regional_options = df_regional['Região'].unique()
    regional = st.selectbox("Regional:", options=sorted(regional_options), index=None)

    # Utilizando a função unique() para obter valores únicos
    area_options = area_dataframe_volume['Área'].unique()
    area = st.selectbox("Área:", options=sorted(area_options), index=None)

    # Utilizando a função unique() para obter valores únicos rotas centencas mostradas na tela
    rota_area_options = area_dataframe_volume['Rota'].unique()
    rota_area = st.selectbox("Rota Área:", options=sorted(rota_area_options), index=None)

    # Utilizando a função unique() para obter valores únicos dos Setores
    setor_optons = dataframe_volume['Setor'].unique()
    setor = st.selectbox("Setor:", options=sorted(setor_optons), index=None)

    # Filtrar as rotas com base no setor selecionado e organizar do menor para o maior
    rotas_do_setor = sorted(dataframe_volume[dataframe_volume['Setor'] == setor]['Rota'].unique())

    # Buscar dados por rota
    rota = st.selectbox(
        "Rota:",
        options=rotas_do_setor, index=None,
    )

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
        background_color = 'Red' if value == 0 else ''
        font_color = 'white' if value == 0 else ''
        return f'background-color: {background_color}; color: {font_color}'


def highlight_zeros(value):
    return 'background-color: Red' if value == 0 else ''


# --------------------------------------------- REGIONAL --------------------------------------------------

if regional:
    st.subheader(f'Vendas Volume Regional: {regional} 📦')
else:
    st.write()

if regional and not (rota_area or secao or (rota_area and secao)):
    df_regional = df_regional[df_regional['Região'] == regional]

    # Agrupar DataFrame
    df_regional = df_regional.groupby(['Região', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    df_regional['Diferença'] = (df_regional['Realizado'] - df_regional['Meta']).round(2)

    # Adicionar a coluna 'Perc. %'
    df_regional['Perc. %'] = ((df_regional['Realizado'] / df_regional['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    df_regional.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df = (
        df_regional.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela
    st.table(styled_df)

# ---------------------------------------------- FIM REGIONAL ------------------------------------------------#


#---------------------------------------------- AREAS --------------------------------------------------------#

if area:
    st.subheader(f'Vendas Volume Área: {area} 📦')
else:
    st.write()

if area and not (rota_area or secao or (rota_area and secao)):
    area_dataframe_filtered = area_dataframe_volume[area_dataframe_volume['Área'] == area]

    # Agrupar DataFrame
    grouped_df = area_dataframe_filtered.groupby(['Área', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df['Diferença'] = (grouped_df['Realizado'] - grouped_df['Meta']).round(2)

    # Adicionar a coluna 'Perc. %'
    grouped_df['Perc. %'] = ((grouped_df['Realizado'] / grouped_df['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_df.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df = (
        grouped_df.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
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
        grouped_df_area_rota['Perc. %'] = ((grouped_df_area_rota['Realizado'] / grouped_df_area_rota['Meta']) * 100).round(2)

        # Remove as linhas que contem nan
        grouped_df_area_rota.dropna(inplace=True)

        # Criar DataFrame com as estilizações
        styled_df_area_rota = (
            grouped_df_area_rota.style
                .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
                .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
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
    grouped_df_area_rota_secao['Perc. %'] = (
            (grouped_df_area_rota_secao['Realizado'] / grouped_df_area_rota_secao['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_df_area_rota_secao.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df_area_rota_secao = (
        grouped_df_area_rota_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
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
    grouped_df_area_secao['Perc. %'] = ((grouped_df_area_secao['Realizado'] / grouped_df_area_secao['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_df_area_secao.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df_area_secao = (
        grouped_df_area_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}',  'Perc. %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela estilizada
    st.table(styled_df_area_secao)

#---------------------------------------------- FIM AREAS --------------------------------------------------------#

# ------------------------------------------- LÓGICA SETORES ---------------------------------------------------- #

# Tabela de Volume por Grupo
tabela_volume_por_grupo = pd.DataFrame()

if setor:
    st.subheader(f'Vendas Volume Setor: {setor} 📦')
else:
    st.write()


# Início Filtros Setores
if setor and not (rota or secao or (rota and secao)):
    tabela_volume_por_grupo = dataframe_volume.loc[
        (dataframe_volume['Setor'] == setor)
    ]

    # Remover a rota
    tabela_volume_por_grupo = tabela_volume_por_grupo.drop(columns=['Rota'])

    # Agrupar
    grouped_setor_df = tabela_volume_por_grupo.groupby(['Área', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_setor_df['Diferença'] = (grouped_setor_df['Realizado'] - grouped_setor_df['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_setor_df['Perc. %'] = (
                (grouped_setor_df['Realizado'] / grouped_setor_df['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_setor_df.dropna(inplace=True)

    # Criar dataframe styler
    styled_df_setor = (
        grouped_setor_df.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
            .hide_index()
    )

    st.table(styled_df_setor)

# if setor e Rota

if setor and rota and not (area or secao or (rota and secao)):
    tabela_volume_por_grupo = dataframe_volume.loc[
        (dataframe_volume['Setor'] == setor) &
        (dataframe_volume['Rota'] == rota)
        # (dataframe_volume ['Área'] == area)
    ]

    # Agrupar
    grouped_setor_rota_df = tabela_volume_por_grupo.groupby(['Rota', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_setor_rota_df['Diferença'] = (grouped_setor_rota_df['Realizado'] - grouped_setor_rota_df['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_setor_rota_df['Perc. %'] = (
                (grouped_setor_rota_df['Realizado'] / grouped_setor_rota_df['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_setor_rota_df.dropna(inplace=True)

    # Criar dataframe styler
    styled_df_setor_rota = (
        grouped_setor_rota_df.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
            .hide_index()
    )

    st.table(styled_df_setor_rota)

# Verificar se 'Setor', 'Rota' e 'Seçao' são verdadeiros
elif setor and rota and secao:
    # Filtrar DataFrame pelo Setor, rota e seção
    tabela_volume_por_grupo = dataframe_volume.loc[
        (dataframe_volume['Setor'] == setor) &
        (dataframe_volume['Rota'] == rota) &
        (dataframe_volume['Seção'] == secao)
        ]

    # Agrupar DataFrame filtrado
    grouped_df_setor_rota_secao = tabela_volume_por_grupo.groupby(['Rota', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df_setor_rota_secao['Diferença'] = (grouped_df_setor_rota_secao['Realizado']-grouped_df_setor_rota_secao['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_df_setor_rota_secao['Perc. %'] = (
            (grouped_df_setor_rota_secao['Realizado'] / grouped_df_setor_rota_secao['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_df_setor_rota_secao.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df_grouped_df_setor_rota_secao = (
        grouped_df_setor_rota_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}', 'Perc. %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela estilizada
    st.table(styled_df_grouped_df_setor_rota_secao)


# Verificar se 'Setor', 'secao'  são verdadeiros
elif setor and secao and not rota:
    # Filtrar DataFrame pelo Setor, seção
    tabela_volume_por_grupo = dataframe_volume.loc[
        (dataframe_volume['Setor'] == setor) &
        (dataframe_volume['Seção'] == secao)
        ]

    # Remover a coluna 'Rota' do DataFrame filtrado
    grouped_df_setor_secao = tabela_volume_por_grupo.drop(columns=['Rota'])

    # Agrupar DataFrame filtrado
    grouped_df_setor_secao = tabela_volume_por_grupo.groupby(['Setor', 'Grupo']).agg({
        'Realizado': 'sum',
        'Meta': 'sum'
    }).reset_index()

    # Adicionar a coluna 'Diferença'
    grouped_df_setor_secao['Diferença'] = (grouped_df_setor_secao['Realizado'] - grouped_df_setor_secao['Meta']).round(2)

    # Adicionar a coluna 'Percentual'
    grouped_df_setor_secao['Perc. %'] = ((grouped_df_setor_secao['Realizado'] / grouped_df_setor_secao['Meta']) * 100).round(2)

    # Remove as linhas que contem nan
    grouped_df_setor_secao.dropna(inplace=True)

    # Criar DataFrame com as estilizações
    styled_df_grouped_df_setor_secao = (
        grouped_df_setor_secao.style
            .applymap(highlight_zeros, subset=pd.IndexSlice[:, ['Realizado']])
            .format({'Realizado': '{:.2f}', 'Meta': '{:.2f}', 'Diferença': '{:.2f}',  'Perc. %': '{:.2f}'})
            .hide_index()
    )

    # Exibir a tabela estilizada
    st.table(styled_df_grouped_df_setor_secao)

# ------------------------------------------- FIM LÓGICA SETORES ---------------------------------------------------- #

# ------------------------------------------- FATURAMENTO ---------------------------------------------------- #

with open('packages.txt', 'w') as packages:
    packages.write('locales-all\n')

import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

df_faturamento = busca_df_faturamento()

fat_setor = df_faturamento.drop(
    columns=['Par/Impar', 'Fornecedor', 'Base Cli.', '1-Realizado',
             '2-Anterior', '(1-2) - Diferença', '.%.', 'branco', '(4-5) Diferença', '%.', 'branco1', '8-Realizado',
             '(8-9) Diferença', '9-Meta', '(8-9) Diferença', '.%', 'branco2', 'ST', 'SM', 'Tend. %',
             ])

# buscando a meta do consultor
meta_faturamento_setor = fat_setor.loc[fat_setor['Setor'] == setor, 'Meta'].sum()
meta_faturamento_area = fat_setor.loc[fat_setor['Área'] == area, 'Meta'].sum()
meta_faturamento_regional = df_regional_fat.loc[df_regional_fat['Região'] == regional, 'Meta'].sum()

# Formatando o formato da meta para 2 casas decimais
# meta_formatada = f"R$ {meta_faturamento_setor:,.2f}"
meta_formatada = locale.currency(meta_faturamento_setor, grouping=True, symbol='R$')
meta_formatada_area = locale.currency(meta_faturamento_area, grouping=True, symbol='R$')
meta_formatada_regional = locale.currency(meta_faturamento_regional, grouping=True, symbol='R$')


# buscando a faturamento do setor
faturamento_setor = fat_setor.loc[fat_setor['Setor'] == setor, 'Realizado'].sum()
faturamento_area = fat_setor.loc[fat_setor['Área'] == area, 'Realizado'].sum()
faturamento_regional = df_regional_fat.loc[df_regional_fat['Região'] == regional, 'Realizado'].sum()

# Formatando o formato da faturamento por setor para 2 casas decimais
# fat_setor_formatada = f"R$ {faturamento_setor:,.2f}"
fat_setor_formatada = locale.currency(faturamento_setor, grouping=True, symbol='R$')
fat_area_formatada = locale.currency(faturamento_area, grouping=True, symbol='R$')
fat_regional_formatada = locale.currency(faturamento_regional, grouping=True, symbol='R$')

# calculo de difereça
diferenca = faturamento_setor - meta_faturamento_setor
diferenca_area = faturamento_area - meta_faturamento_area
diferenca_regional = faturamento_regional - meta_faturamento_regional

# diferenca_formatada = f"R$ {diferenca:,.2f}"
diferenca_formatada = locale.currency(diferenca, grouping=True, symbol='R$')
diferenca_formatada_area = locale.currency(diferenca_area, grouping=True, symbol='R$')
diferenca_formatada_regional = locale.currency(diferenca_regional, grouping=True, symbol='R$')



# calculando a porcentagem
porcentagem_meta_setor = round(faturamento_setor / meta_faturamento_setor * 100, 2)
porcentagem_meta_area = round(faturamento_area / meta_faturamento_area * 100, 2)
porcentagem_meta_rerional = round(faturamento_regional / meta_faturamento_regional * 100, 2)


if setor:
    #____________________Setores__________________#
    st.markdown("---")
    st.subheader(f'Faturamendo Setor: {setor} 💰')

    col1, col2, col3, col4, = st.columns([1, 1, 1, 1])

    with col1:
        st.write('**META**')
        st.info(meta_formatada)

    with col2:
        st.write('**FATURAMENTO**')
        st.info(fat_setor_formatada)

    with col3:
        st.write('**DIFERENÇA**')
        st.info(diferenca_formatada)

    with col4:
        st.write('**Perc.%**')
        st.info(porcentagem_meta_setor)

    st.markdown("---")
    # ____________________Setores__________________#

    # ____________________Area__________________#
elif area:
    st.markdown("---")
    st.subheader(f'Faturamendo Área: {area} 💰')

    col1, col2, col3, col4, = st.columns([1, 1, 1, 1])

    with col1:
        st.write('**META**')
        st.info(meta_formatada_area)

    with col2:
        st.write('**FATURAMENTO**')
        st.info(fat_area_formatada)

    with col3:
        st.write('**DIFERENÇA**')
        st.info(diferenca_formatada_area)

    with col4:
        st.write('**Perc.%**')
        st.info(porcentagem_meta_area)

    st.markdown("---")

    # ____________________Area__________________#


    # ____________________Regionais__________________#
elif regional:
    st.markdown("---")
    st.subheader(f'Faturamendo Regional: {regional} 💰')

    col1, col2, col3, col4, = st.columns([1, 1, 1, 1])

    with col1:
        st.write('**META**')
        st.info(meta_formatada_regional)

        with col2:
            st.write('**FATURAMENTO**')
            st.info(fat_regional_formatada)

        with col3:
            st.write('**DIFERENÇA**')
            st.info(diferenca_formatada_regional)

        with col4:
            st.write('**Perc.%**')
            st.info(porcentagem_meta_rerional)

    st.markdown("---")



    # ____________________Regionais__________________#



else:
    st.write()

