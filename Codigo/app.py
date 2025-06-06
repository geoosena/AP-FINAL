import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    layout="wide", 
    page_title="Shein Insights: Preços & Descontos", 
    page_icon="🍭"
)

# Estilo
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffc0cb;
        color: black;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton > button {
        background-color: black;
        color: #ffc0cb;
        border: none;
    }
    .stButton > button:hover {
        background-color: #333333;
        color: #ff99bb;
    }
    .stTextInput>div>input, .stSlider>div>input {
        border: 1px solid black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Shein Insights: Preços & Descontos")
st.markdown("Explore os **preços e descontos** dos produtos da Shein de forma interativa.")

# Leitura dos dados
caminho_dados = 'Bases tratadas/dados_shein_tratado.csv'

try:
    df = pd.read_csv(caminho_dados, sep=';')
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

# Tratamento das colunas
df['preco2'] = df['preco2'].astype(str).str.replace('R\$', '', regex=True).str.replace(',', '.').astype(float)
df['desconto'] = df['desconto'].fillna('0').astype(str)
df['desconto'] = df['desconto'].str.replace('%', '', regex=True).str.replace('-', '0').str.strip()
df['desconto'] = pd.to_numeric(df['desconto'], errors='coerce').fillna(0)

# Diagnóstico para verificar o que é preco2 e desconto
st.subheader("🕵️ Diagnóstico de Preços e Descontos")
st.write("🔍 Primeiras linhas da base para análise de valores:")
st.write(df[['preco2', 'desconto']].head(10))

# Estimativa do preço original
df['preco_original_estimado'] = df['preco2'] + df['desconto']
st.write("💡 Preço original estimado (preco2 + desconto):")
st.write(df[['preco2', 'desconto', 'preco_original_estimado']].head(10))

# Cálculo do desconto percentual (assumindo que preco2 é o valor COM desconto)
df['desconto_percentual'] = (df['desconto'] / (df['preco2'] + df['desconto'])) * 100

# Filtro por faixa de preço
preco_min, preco_max = df['preco2'].min(), df['preco2'].max()
preco_range = st.slider(
    "🔎 Filtrar por faixa de preço (R$):", 
    min_value=float(preco_min), 
    max_value=float(preco_max), 
    value=(float(preco_min), float(preco_max))
)

df_filtrado = df[(df['preco2'] >= preco_range[0]) & (df['preco2'] <= preco_range[1])]

# Criação de faixas de preço
bins = pd.cut(df_filtrado['preco2'], bins=5)
labels = [f"R${round(interval.left,2)} - R${round(interval.right,2)}" for interval in bins.cat.categories]
df_filtrado['faixa_preco'] = pd.cut(df_filtrado['preco2'], bins=5, labels=labels)

# Resumo estatístico
st.subheader("📄 Resumo Estatístico dos Dados Filtrados")
st.write(df_filtrado[['preco2', 'desconto', 'desconto_percentual']].describe())

# Variáveis numéricas para gráficos
variaveis_numericas = ['preco2', 'desconto', 'desconto_percentual']

# Gráficos Univariados
st.subheader("📊 Gráficos Univariados")
col1, col2 = st.columns(2)

with col1:
    var_hist = st.selectbox("Variável para o Histograma:", variaveis_numericas, index=0)
    st.markdown(f"**Histograma de {var_hist}**")
    fig1, ax1 = plt.subplots()
    sns.histplot(df_filtrado[var_hist], bins=20, ax=ax1, color='black')
    ax1.set_xlabel(var_hist)
    st.pyplot(fig1)

wi
