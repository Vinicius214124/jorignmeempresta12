import requests
import json
import time
import datetime
import pymysql
import base64
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import folium
import streamlit.components.v1 as components
from collections import Counter
from folium.plugins import HeatMap
import streamlit as st




 
st.set_page_config(page_title="Dashboard de Clientes - RealsBet", page_icon="📊", layout="wide")



 
st.markdown(
    """
    <style>
    .card { 
        background: linear-gradient(135deg, #181a1f, #262930);
        border-radius: 12px;
        padding: 20px;
        margin: 15px;
        box-shadow: 0px 5px 15px rgba(2, 253, 169, 0.4);
        transition: all 0.3s ease-in-out;
    }
    .card:hover { transform: scale(1.03); }
    .card-header { 
        font-size: 22px; 
        font-weight: bold; 
        color: #02FDA9; 
        text-transform: uppercase;
    }
    .card-value { 
        font-size: 36px; 
        font-weight: bold; 
        color: #9B58CC; 
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)



 
# 🔍 Configuração do Banco de Dados
DB_CONFIG = {
    "user": "matheus.maia",
    "password": "QI5I4z2li7",
    "host": "afiliados.cluster-c9amokse62za.us-east-1.rds.amazonaws.com",
    "port": 3306,
    "database": "afiliados",
    "connect_timeout": 10
}
 
# 🔍 Função para obter os dados do MySQL (dados de clientes)
def obter_dados():
    query = """
        SELECT
        c.id,
        c.first_name,
        c.merchant_id,
        c.registration_date  -- ✅ Remova a vírgula extra!
    FROM afiliados.clients c
    WHERE
        c.merchant_id = '9cfe84e1-21be-4c3d-8f9d-d1fdc9add648'
        AND c.registration_date >= '2025-01-01'
    """
    try:
        connection = pymysql.connect(**DB_CONFIG)
        connection.ping(reconnect=True)
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except pymysql.MySQLError as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return None
    except Exception as e:
        st.error(f"Erro ao obter dados: {e}")
        return None
 
# 🔍 Função para obter os dados de DDD e regiões/cidades
def obter_dados_ddd():
    query = """
    SELECT DISTINCT
    c.external_id,
    c.phone_number,
    c.registration_date,
    CASE
        WHEN LENGTH(IFNULL(c.phone_number, '')) < 4 THEN 'Número Inválido'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '11' THEN 'São Paulo - Capital e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '12' THEN 'Vale do Paraíba e Litoral Norte'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '13' THEN 'Baixada Santista e Litoral Sul'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '14' THEN 'Bauru e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '15' THEN 'Sorocaba e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '16' THEN 'Ribeirão Preto e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '17' THEN 'São José do Rio Preto e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '18' THEN 'Presidente Prudente e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '19' THEN 'Campinas e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '21' THEN 'Rio de Janeiro - Capital e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '22' THEN 'Norte Fluminense'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '24' THEN 'Sul Fluminense'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '27' THEN 'Grande Vitória e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '28' THEN 'Sul do Espírito Santo'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '31' THEN 'Belo Horizonte e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '32' THEN 'Zona da Mata'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '33' THEN 'Leste de Minas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '34' THEN 'Triângulo Mineiro'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '35' THEN 'Sul de Minas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '37' THEN 'Centro-Oeste de Minas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '38' THEN 'Norte de Minas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '41' THEN 'Curitiba e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '42' THEN 'Centro-Sul do Paraná'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '43' THEN 'Norte do Paraná'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '44' THEN 'Noroeste do Paraná'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '45' THEN 'Oeste do Paraná'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '46' THEN 'Sudoeste do Paraná'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '47' THEN 'Norte de Santa Catarina'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '48' THEN 'Grande Florianópolis e Sul de SC'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '49' THEN 'Oeste de Santa Catarina'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '51' THEN 'Porto Alegre e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '53' THEN 'Sul do Rio Grande do Sul'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '54' THEN 'Serra Gaúcha'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '55' THEN 'Centro-Oeste do Rio Grande do Sul'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '61' THEN 'Distrito Federal'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '62' THEN 'Goiânia e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '63' THEN 'Tocantins'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '64' THEN 'Sul de Goiás'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '65' THEN 'Cuiabá e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '66' THEN 'Interior do Mato Grosso'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '67' THEN 'Mato Grosso do Sul'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '68' THEN 'Acre'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '69' THEN 'Rondônia'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '91' THEN 'Região Metropolitana de Belém'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '92' THEN 'Manaus e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '93' THEN 'Oeste do Pará'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '94' THEN 'Sudeste do Pará'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '95' THEN 'Roraima'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '96' THEN 'Amapá'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '97' THEN 'Interior do Amazonas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '98' THEN 'São Luís e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '99' THEN 'Interior do Maranhão'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '71' THEN 'Salvador e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '73' THEN 'Sul da Bahia'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '74' THEN 'Norte da Bahia'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '75' THEN 'Recôncavo Baiano'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '77' THEN 'Oeste da Bahia'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '79' THEN 'Sergipe'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '81' THEN 'Recife e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '82' THEN 'Alagoas'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '83' THEN 'Paraíba'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '84' THEN 'Rio Grande do Norte'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '85' THEN 'Fortaleza e Região Metropolitana'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '86' THEN 'Teresina e Região'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '87' THEN 'Interior de Pernambuco'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '88' THEN 'Interior do Ceará'
        WHEN SUBSTRING(c.phone_number, 4, 2) = '89' THEN 'Sul do Piauí'
        ELSE 'Outro'
    END AS ddd_cidade_regiao,
    c.status
FROM afiliados.clients c
WHERE
    c.merchant_id = '9cfe84e1-21be-4c3d-8f9d-d1fdc9add648'
    AND c.registration_date >= '2025-01-01';
    """
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        connection.ping(reconnect=True)
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except pymysql.MySQLError as e:
        st.error(f"Erro ao conectar com o banco de dados: {e}")
        return None


 
# 🧮 Função para calcular o total de registros desde o começo do ano e o total de registros do dia
def calcular_totais(dados):
    total_registros_ano = len(dados)
    total_registros_dia = dados[dados['registration_date'].dt.date == datetime.datetime.today().date()].shape[0]
    return total_registros_ano, total_registros_dia
 
# 🏷️ Função para calcular a data do último registro
def obter_ultimo_registro(dados):
    if dados is not None and not dados.empty:
        ultimo_registro = dados['registration_date'].max()
        return ultimo_registro
    return None

# 🔍 Baixar GeoJSON do Brasil (fronteiras)
def obter_geojson_brasil():
    url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Inicializa a variável para armazenar a cidade selecionada
if 'cidade_selecionada' not in st.session_state:
    st.session_state.cidade_selecionada = None

def selecionar_cidade(cidade):
    st.session_state.cidade_selecionada = cidade
    st.session_state.dados_filtrados = dados_ddd[dados_ddd['ddd_cidade_regiao'] == cidade]

    # Criar o botão de exportação para Excel
    if not st.session_state.dados_filtrados.empty:
        exportar_para_excel(st.session_state.dados_filtrados[['external_id']], f"{cidade.replace(' ', '_')}.xlsx")


siglas_estados = {
    "AC": [-9.02, -70.81], "AL": [-9.57, -36.53], "AM": [-3.47, -65.10], "AP": [1.41, -51.77], "BA": [-12.97, -41.54],
    "CE": [-5.20, -39.53], "DF": [-15.78, -47.93], "ES": [-19.19, -40.34], "GO": [-15.98, -49.86], "MA": [-5.42, -45.44],
    "MG": [-18.10, -44.38], "MS": [-20.51, -54.54], "MT": [-12.64, -55.42], "PA": [-3.79, -52.48], "PB": [-7.28, -36.72],
    "PE": [-8.38, -37.86], "PI": [-7.70, -42.74], "PR": [-24.89, -51.55], "RJ": [-22.84, -43.15], "RN": [-5.79, -36.59],
    "RO": [-10.88, -63.28], "RR": [2.05, -61.34], "RS": [-30.03, -53.44], "SC": [-27.45, -50.95], "SE": [-10.57, -37.44],
    "SP": [-22.19, -48.79], "TO": [-10.25, -48.30]
}


# Mapeamento de cidades/regiões para estados
mapa_cidades_estados = {
    "São Paulo - Capital e Região Metropolitana": "SP",
    "Vale do Paraíba e Litoral Norte": "SP",
    "Baixada Santista e Litoral Sul": "SP",
    "Bauru e Região": "SP",
    "Sorocaba e Região": "SP",
    "Ribeirão Preto e Região": "SP",
    "São José do Rio Preto e Região": "SP",
    "Presidente Prudente e Região": "SP",
    "Campinas e Região": "SP",
    "Rio de Janeiro - Capital e Região Metropolitana": "RJ",
    "Norte Fluminense": "RJ",
    "Sul Fluminense": "RJ",
    "Grande Vitória e Região": "ES",
    "Sul do Espírito Santo": "ES",
    "Belo Horizonte e Região Metropolitana": "MG",
    "Zona da Mata": "MG",
    "Leste de Minas": "MG",
    "Triângulo Mineiro": "MG",
    "Sul de Minas": "MG",
    "Centro-Oeste de Minas": "MG",
    "Norte de Minas": "MG",
    "Curitiba e Região Metropolitana": "PR",
    "Centro-Sul do Paraná": "PR",
    "Norte do Paraná": "PR",
    "Noroeste do Paraná": "PR",
    "Oeste do Paraná": "PR",
    "Sudoeste do Paraná": "PR",
    "Norte de Santa Catarina": "SC",
    "Grande Florianópolis e Sul de SC": "SC",
    "Oeste de Santa Catarina": "SC",
    "Porto Alegre e Região Metropolitana": "RS",
    "Sul do Rio Grande do Sul": "RS",
    "Serra Gaúcha": "RS",
    "Centro-Oeste do Rio Grande do Sul": "RS",
    "Distrito Federal": "DF",
    "Goiânia e Região": "GO",
    "Tocantins": "TO",
    "Sul de Goiás": "GO",
    "Cuiabá e Região": "MT",
    "Interior do Mato Grosso": "MT",
    "Mato Grosso do Sul": "MS",
    "Acre": "AC",
    "Rondônia": "RO",
    "Região Metropolitana de Belém": "PA",
    "Manaus e Região": "AM",
    "Oeste do Pará": "PA",
    "Sudeste do Pará": "PA",
    "Roraima": "RR",
    "Amapá": "AP",
    "Interior do Amazonas": "AM",
    "São Luís e Região": "MA",
    "Interior do Maranhão": "MA",
    "Salvador e Região Metropolitana": "BA",
    "Sul da Bahia": "BA",
    "Norte da Bahia": "BA",
    "Recôncavo Baiano": "BA",
    "Oeste da Bahia": "BA",
    "Sergipe": "SE",
    "Recife e Região Metropolitana": "PE",
    "Alagoas": "AL",
    "Paraíba": "PB",
    "Rio Grande do Norte": "RN",
    "Fortaleza e Região Metropolitana": "CE",
    "Teresina e Região": "PI",
    "Interior de Pernambuco": "PE",
    "Interior do Ceará": "CE",
    "Sul do Piauí": "PI",
}



def gerar_mapa(dados):
    estado_count = Counter(dados['ddd_cidade_regiao'])

    # Mapa com tema escuro (Carto Dark)
    mapa = folium.Map(
        location=[-14.2350, -51.9253],
        zoom_start=4,
        max_bounds=True,
        control_scale=True,
        tiles="CartoDB dark_matter"
    )

    # ✅ Adiciona as linhas brancas ao redor do Brasil
    geojson_brasil = obter_geojson_brasil()
    if geojson_brasil:
        folium.GeoJson(
            geojson_brasil,
            name="Fronteiras do Brasil",
            style_function=lambda feature: {
                "fillColor": "transparent",
                "color": "white",
                "weight": 1.5,
                "fillOpacity": 0.2
            }
        ).add_to(mapa)

    # 🔥 Adiciona as siglas dos estados dentro dos polígonos
    for sigla, coord in siglas_estados.items():
        folium.Marker(
            location=coord,
            icon=folium.DivIcon(
                html=f'<div style="font-size: 10px; font-weight: bold; color: white; opacity: 0.7;">{sigla}</div>'
            )
        ).add_to(mapa)

    # ✅ Loop para adicionar todas as bolinhas corretamente
    for estado, count in estado_count.items():
        if estado in geolocalizacao:
            dados_filtrados = dados[dados['ddd_cidade_regiao'] == estado]

            popup_html = f"""
            <div style="background: white;
                        color: black;
                        padding: 12px;
                        border-radius: 12px;
                        box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.3);
                        font-size: 14px;
                        text-align: center;
                        font-family: 'Arial', sans-serif;">
                
                <h4 style="color: #333; margin-bottom: 6px;">{estado}</h4>
                
                <hr style="border-top: 1px solid #ddd; margin: 5px 0;">
                
                <b>Registros:</b> <span style="color: #27ae60; font-size: 16px;">{count}</span>
            
            </div>
            """

            folium.CircleMarker(
                location=geolocalizacao[estado],
                radius=5 + (count / 200),  # 🔥 Faz as bolinhas ficarem maiores conforme o volume de registros
                color='#00acc1',
                weight=2,
                fill=True,
                fill_color='#02FDA9 ',
                fill_opacity=0.85,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{estado} - {count} registros"
            ).add_to(mapa)

    return mapa


def exportar_para_excel(df, nome_arquivo="dados_exportados.xlsx"):
    """
    Exporta um DataFrame para um arquivo Excel e retorna um link de download no Streamlit.
    """
    if df is None or df.empty:
        st.warning("Nenhum dado disponível para exportação.")
        return None

    nome_arquivo_path = f"./{nome_arquivo}"
    # ✅ Incluir phone_number e registration_date na exportação
    colunas_disponiveis = [col for col in ['external_id', 'phone_number', 'registration_date'] if col in df.columns]
    df[colunas_disponiveis].to_excel(nome_arquivo_path, index=False)


    with open(nome_arquivo_path, "rb") as f:
        st.download_button(
            label="📥 Baixar Excel",
            data=f,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


def exportar_por_estado(estado_sigla):
    """
    Exporta os registros de todas as cidades pertencentes a um estado.
    """
    cidades_do_estado = [cidade for cidade, estado in mapa_cidades_estados.items() if estado == estado_sigla]
    dados_estado = dados_ddd[dados_ddd['ddd_cidade_regiao'].isin(cidades_do_estado)]

    if dados_estado.empty:
        st.warning(f"Nenhum dado disponível para exportação no estado {estado_sigla}.")
        return None

    nome_arquivo = f"{estado_sigla}_registros.xlsx"
    nome_arquivo_path = f"./{nome_arquivo}"

    # ✅ Incluir phone_number e registration_date na exportação
    dados_estado[['external_id', 'phone_number', 'registration_date']].to_excel(nome_arquivo_path, index=False)

    with open(nome_arquivo_path, "rb") as f:
        st.download_button(
            label=f"📥 Baixar registros de {estado_sigla}",
            data=f,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

geolocalizacao = {
    # São Paulo
    'São Paulo - Capital e Região Metropolitana': [-23.5505, -46.6333],
    'Vale do Paraíba e Litoral Norte': [-23.2237, -45.8919],
    'Baixada Santista e Litoral Sul': [-24.0058, -46.4026],
    'Bauru e Região': [-22.3145, -49.0605],
    'Sorocaba e Região': [-23.5015, -47.4581],
    'Ribeirão Preto e Região': [-21.1775, -47.8103],
    'São José do Rio Preto e Região': [-20.8113, -49.3758],
    'Presidente Prudente e Região': [-22.1256, -51.3925],
    'Campinas e Região': [-22.9056, -47.0608],

    # Rio de Janeiro
    'Rio de Janeiro - Capital e Região Metropolitana': [-22.9068, -43.1729],
    'Norte Fluminense': [-21.6400, -41.0511],
    'Sul Fluminense': [-22.5140, -44.1042],

    # Espírito Santo
    'Grande Vitória e Região': [-20.3155, -40.3128],
    'Sul do Espírito Santo': [-21.1261, -41.6737],

    # Minas Gerais
    'Belo Horizonte e Região Metropolitana': [-19.8157, -43.9542],
    'Zona da Mata': [-21.7581, -43.3496],
    'Leste de Minas': [-19.5197, -41.0645],
    'Triângulo Mineiro': [-18.9186, -48.2768],
    'Sul de Minas': [-22.2569, -45.7039],
    'Centro-Oeste de Minas': [-20.1385, -44.8887],
    'Norte de Minas': [-16.7279, -43.8631],

    # Paraná
    'Curitiba e Região Metropolitana': [-25.4284, -49.2733],
    'Centro-Sul do Paraná': [-25.6934, -51.6571],
    'Norte do Paraná': [-23.3103, -51.1628],
    'Noroeste do Paraná': [-23.7665, -52.2506],
    'Oeste do Paraná': [-24.5432, -54.5784],
    'Sudoeste do Paraná': [-26.2273, -52.6701],

    # Santa Catarina
    'Norte de Santa Catarina': [-26.3045, -48.8486],
    'Grande Florianópolis e Sul de SC': [-27.5954, -48.5480],
    'Oeste de Santa Catarina': [-27.1004, -51.6182],

    # Rio Grande do Sul
    'Porto Alegre e Região Metropolitana': [-30.0346, -51.2177],
    'Sul do Rio Grande do Sul': [-31.7697, -52.3425],
    'Serra Gaúcha': [-29.1842, -51.5194],
    'Centro-Oeste do Rio Grande do Sul': [-28.6461, -54.0399],

    # Centro-Oeste
    'Distrito Federal': [-15.7801, -47.9292],
    'Goiânia e Região': [-16.6809, -49.2533],
    'Tocantins': [-10.1843, -48.3334],
    'Sul de Goiás': [-17.7946, -50.9181],
    'Cuiabá e Região': [-15.6014, -56.0979],
    'Interior do Mato Grosso': [-12.6819, -55.6950],
    'Mato Grosso do Sul': [-20.4697, -54.6201],

    # Norte
    'Acre': [-9.9749, -67.8101],
    'Rondônia': [-8.7611, -63.9039],
    'Região Metropolitana de Belém': [-1.4550, -48.5024],
    'Manaus e Região': [-3.1190, -60.0217],
    'Oeste do Pará': [-2.4385, -54.6996],
    'Sudeste do Pará': [-5.3811, -49.1327],
    'Roraima': [2.8192, -60.6736],
    'Amapá': [0.0372, -51.0705],
    'Interior do Amazonas': [-5.1461, -63.6280],
    'São Luís e Região': [-2.5387, -44.2825],
    'Interior do Maranhão': [-5.5263, -45.1240],

    # Nordeste
    'Salvador e Região Metropolitana': [-12.9714, -38.5014],
    'Sul da Bahia': [-14.7903, -39.2787],
    'Norte da Bahia': [-10.9616, -40.5126],
    'Recôncavo Baiano': [-12.6810, -39.1170],
    'Oeste da Bahia': [-12.5797, -44.0560],
    'Sergipe': [-10.9472, -37.0731],
    'Recife e Região Metropolitana': [-8.0476, -34.8770],
    'Alagoas': [-9.5713, -36.7819],
    'Paraíba': [-7.1216, -35.2659],
    'Rio Grande do Norte': [-5.7945, -35.2110],
    'Fortaleza e Região Metropolitana': [-3.7172, -38.5433],
    'Teresina e Região': [-5.0920, -42.8038],
    'Interior de Pernambuco': [-8.7494, -36.6468],
    'Interior do Ceará': [-6.0166, -39.6990],
    'Sul do Piauí': [-8.2866, -43.6803]
}



 
# Carregar dados de clientes e dados de DDD
dados = obter_dados()
dados_ddd = obter_dados_ddd()

# 🔍 Criar gráfico de registros por dia
if dados is not None and not dados.empty:
    dados['day'] = dados['registration_date'].dt.to_period('D')
registros_por_dia = dados.groupby('day').size().reset_index(name='Quantidade de Registros')
registros_por_dia['day'] = registros_por_dia['day'].astype(str)  # Converter para string para exibição correta

fig_dia = go.Figure()

fig_dia.add_trace(go.Bar(
    x=registros_por_dia['day'],
    y=registros_por_dia['Quantidade de Registros'],
    marker=dict(color='#02FDA9'),  # Azul mais claro
    name='Registros por Dia'
))


fig_dia.update_layout(
    title="📊 Registros por Dia",
    xaxis_title="📅 Dia",
    yaxis_title="📈 Quantidade",
    plot_bgcolor='#181a1f',
    paper_bgcolor='#181a1f',
    font=dict(color='#eceff1'),
    hovermode="x unified"
)


# Criando o gráfico de registros por mês antes de ser chamado em col3
dados['month'] = dados['registration_date'].dt.to_period('M')
registros_por_mes = dados.groupby('month').size().reset_index(name='Quantidade de Registros')
registros_por_mes['month'] = registros_por_mes['month'].dt.strftime('%b %Y')
registros_por_mes['Quantidade de Registros'] = registros_por_mes['Quantidade de Registros'].apply(lambda x: f"{x:,.0f}")

fig = go.Figure()
# Atualização das cores das barras
fig.add_trace(go.Bar(
    x=registros_por_mes['month'],
    y=registros_por_mes['Quantidade de Registros'],
    marker=dict(color='#9B58CC'),  # Roxo
    name='Registros por Mês'
))



fig.update_layout(
    title="📊 Registros por Mês",
    xaxis_title="📅 Mês",
    yaxis_title="📈 Quantidade",
    plot_bgcolor='#181a1f',
    paper_bgcolor='#181a1f',
    font=dict(color='#02FDA9'),  # Verde nos rótulos
    bargap=0.6,
    xaxis=dict(tickangle=-45),
    height=500
)



if dados is not None and dados_ddd is not None and not dados.empty:
    # Calcular os totais
    total_registros_ano, total_registros_dia = calcular_totais(dados)
    ultimo_registro = obter_ultimo_registro(dados)

# Definição das colunas principais
col1, col2, col3 = st.columns([3, 5, 3])  # 🔥 Aumentei a largura do mapa no centro


st.markdown("""
    <style>
        /* Animação mais suave */
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.9; }
            50% { transform: scale(1.02); opacity: 1; }
            100% { transform: scale(1); opacity: 0.9; }
        }

        .card {
            background: linear-gradient(135deg, #1c1f26, #2a2d36);
            border-radius: 12px;
            padding: 18px;
            text-align: center;
            box-shadow: 0px 4px 10px rgba(0, 255, 0, 0.2);
            transition: all 0.3s ease-in-out;
            animation: pulse 4s infinite;
        }
        .card:hover {
            transform: scale(1.03);
            box-shadow: 0px 6px 12px rgba(0, 255, 0, 0.25);
        }
        .card-title {
            font-size: 20px;
            font-weight: 600;
            color: #00e6ac;
        }
        .card-value {
            font-size: 36px;
            font-weight: 700;
            color: #e0e0e0;
            text-shadow: 1px 1px 3px rgba(0, 255, 0, 0.3);
        }
    </style>
""", unsafe_allow_html=True)

with col1:
    st.markdown(f"""
        <div class="card">
            <div class="card-header">📆 Total de Registros no Ano</div>
            <div class="card-value">{total_registros_ano:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <div class="card-header">📅 Total de Registros no Dia</div>
            <div class="card-value">{total_registros_dia:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="card">
            <div class="card-header">⏳ Último Registro</div>
            <div class="card-value">{ultimo_registro.strftime('%d/%m/%Y %H:%M')}</div>
        </div>
    """, unsafe_allow_html=True)


# Mapa no centro
with col2:
    st.markdown("")
    mapa = gerar_mapa(dados_ddd)
    components.html(mapa._repr_html_(), height=500)  # 🔥 Aumenta a altura do mapa


# Registros por Mês na direita
with col3:
    st.markdown("")
    st.plotly_chart(fig, use_container_width=True)

# Definição da segunda linha de colunas para Ranking e Registros por Dia
col4, col5 = st.columns([3, 4])

# Ranking dos Estados na Esquerda
# Ranking dos Estados na Esquerda (Sempre visível)
with col4:
    st.markdown("## 🏆 Top 10 Estados com Mais Registros")

    if dados_ddd is not None and not dados_ddd.empty:
        ranking_estados = dados_ddd['ddd_cidade_regiao'].value_counts().reset_index()
        ranking_estados.columns = ['Estado', 'Registros']

        fig_ranking = go.Figure()
        fig_ranking.add_trace(go.Bar(
    x=ranking_estados['Registros'].head(10),
    y=ranking_estados['Estado'].head(10),
    orientation='h',
    marker=dict(color='#9B58CC ')  # Azul suave
))

        fig_ranking.update_layout(
    title="🏆 Top 10 Estados com Mais Registros",
    xaxis_title="Quantidade de Registros",
    yaxis_title="Estado",
    plot_bgcolor='#181a1f',
    paper_bgcolor='#181a1f',
    font=dict(color='#eceff1'),
    xaxis=dict(gridcolor="rgba(255, 255, 255, 0.2)"),
    yaxis=dict(categoryorder="total ascending"),
)

        st.plotly_chart(fig_ranking, use_container_width=True)

# Registros por Dia na Direita
with col5:
    st.markdown("")
    st.plotly_chart(fig_dia, use_container_width=True)
    st.markdown(f"📅 Dados atualizados em: {datetime.datetime.today().strftime('%d/%m/%Y')}")

        # 🏆 Ranking de Estados com Mais Registros - Posicionado na Esquerda
st.markdown("### 📊 Estatísticas de Registros")


# Inicializa a variável como um DataFrame vazio para evitar erro de variável não definida
dados_filtrados = pd.DataFrame()

# 🔍 Verifica se uma cidade foi selecionada
if "cidade_selecionada" in st.session_state and st.session_state.cidade_selecionada:
    cidade_selecionada = st.session_state.cidade_selecionada
    st.success(f"📍 Cidade selecionada: {cidade_selecionada}")

    # 🔎 Filtra os dados da cidade selecionada
    dados_filtrados = dados_ddd[dados_ddd['ddd_cidade_regiao'] == cidade_selecionada]

    # ✅ Exportação dos dados da cidade selecionada
    if not dados_filtrados.empty:
        colunas_exportar = ['external_id', 'phone_number', 'registration_date']  # Garante colunas relevantes
        colunas_disponiveis = [col for col in colunas_exportar if col in dados_filtrados.columns]  # Filtra apenas colunas existentes

        if colunas_disponiveis:
            nome_arquivo = f"{cidade_selecionada.replace(' ', '_')}.xlsx"
            dados_filtrados[colunas_disponiveis].to_excel(nome_arquivo, index=False)

            with open(nome_arquivo, "rb") as f:
                st.download_button(
                    label=f"📥 Baixar registros de {cidade_selecionada}",
                    data=f,
                    file_name=nome_arquivo,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("Os dados disponíveis não incluem telefone ou data de registro.")


# 🏷️ Exportação por Estado
st.markdown("""
## 🌎 Exportação de Dados por Estado  
Selecione um estado abaixo para baixar os registros correspondentes.
""", unsafe_allow_html=True)

# Inicializa a variável no session_state caso não exista
if "estado_exportacao" not in st.session_state:
    st.session_state.estado_exportacao = list(siglas_estados.keys())[0]  # Estado padrão

# Criando um seletor sem disparar a atualização
novo_estado = st.radio(
    "🔎 Escolha um estado para exportação:",
    list(siglas_estados.keys()),
    index=list(siglas_estados.keys()).index(st.session_state.estado_exportacao),
    horizontal=True
)

# Apenas altera o estado no session_state sem recarregar a página
if novo_estado != st.session_state.estado_exportacao:
    st.session_state.estado_exportacao = novo_estado  # Atualiza apenas o estado selecionado

# Exibe as opções e o botão de exportação sem travar a aplicação
st.markdown(f"""
    <div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px rgba(0, 255, 0, 0.3); text-align: center;">
        <h4 style="color: #02FDA9 ;">📂 Exportar Dados de {st.session_state.estado_exportacao}</h4>
        <p style="color: white;">Clique abaixo para baixar os registros desse estado.</p>
    </div>
""", unsafe_allow_html=True)

exportar_por_estado(st.session_state.estado_exportacao)  # Chama a função sem recarregar



st.markdown("<hr style='border: 1px solid #02FDA9 ;'>", unsafe_allow_html=True)





# 📱 Estilos para melhor responsividade no Mobile
st.markdown("""
    <style>
    /* Ajuste do layout em telas menores */
    @media only screen and (max-width: 768px) {
        .stApp {
            padding: 5px !important;
        }
        .card {
            width: 100% !important;
            margin: 5px 0 !important;
        }
        .card-header {
            font-size: 18px !important;
        }
        .card-value {
            font-size: 28px !important;
        }
        .stPlotlyChart {
            width: 100% !important;
        }
    }

    /* Estiliza o botão de tela cheia no celular */
    @media only screen and (max-width: 480px) {
        #fullscreen-btn {
            font-size: 14px !important;
            padding: 8px !important;
            width: 100% !important;
            bottom: 10px !important;
            right: 10px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)






# 🏷️ Variáveis de controle de tempo
if "ultimo_registro" not in st.session_state:
    st.session_state.ultimo_registro = datetime.datetime.now()
if "tempo_sem_registros" not in st.session_state:
    st.session_state.tempo_sem_registros = 0

# 🏷️ Variáveis de controle no session_state
if "ultimo_registro" not in st.session_state:
    st.session_state.ultimo_registro = datetime.datetime.now()
if "tempo_sem_registros" not in st.session_state:
    st.session_state.tempo_sem_registros = 0
if "ultima_verificacao" not in st.session_state:
    st.session_state.ultima_verificacao = time.time()

# 🔄 Função para verificar novos cadastros a cada minuto
def verificar_novos_cadastros():
    dados = obter_dados()
    if dados is not None and not dados.empty:
        ultimo_registro = dados['registration_date'].max()

        if ultimo_registro > st.session_state.ultimo_registro:
            st.session_state.ultimo_registro = ultimo_registro
            st.session_state.tempo_sem_registros = 0  # Reinicia o contador
        else:
            st.session_state.tempo_sem_registros += 1  # Incrementa a cada minuto sem novo cadastro

    # 🚨 Alerta no terminal após 50 minutos sem novos cadastros
    if st.session_state.tempo_sem_registros >= 50:
        print("🚨 ALERTA: Nenhum novo cadastro foi registrado nos últimos 50 minutos!")

# ⏳ Verifica se já passou 1 minuto desde a última atualização
if time.time() - st.session_state.ultima_verificacao > 60:
    verificar_novos_cadastros()
    st.session_state.ultima_verificacao = time.time()
    st.rerun()  # Atualiza a dashboard automaticamente