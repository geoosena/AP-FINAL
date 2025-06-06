import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(
    layout="wide", 
    page_title="Shein Insights: Preços & Descontos", 
    page_icon="🍭"
)

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

caminho_dados = 'Bases tratadas/dados_shein_tratado.csv'

try:
    df = pd.read_csv(caminho_dados, sep=';')
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

df['preco2'] = df['preco2'].astype(str).str.replace('R\$', '', regex=True).str.replace(',', '.').astype(float)
df['desconto'] = df['desconto'].fillna('0').astype(str)
df['desconto'] = df['desconto'].str.replace('%', '', regex=True).str.replace('-', '0').str.strip()
df['desconto'] = pd.to_numeric(df['desconto'], errors='coerce').fillna(0)
df['desconto_percentual'] = (df['desconto'] / (df['preco2'] + df['desconto'])) * 100

preco_min, preco_max = df['preco2'].min(), df['preco2'].max()
preco_range = st.slider(
    "🔎 Filtrar por faixa de preço (R$):", 
    min_value=float(preco_min), 
    max_value=float(preco_max), 
    value=(float(preco_min), float(preco_max))
)

df_filtrado = df[(df['preco2'] >= preco_range[0]) & (df['preco2'] <= preco_range[1])]

# Novo filtro de colunas
colunas_disponiveis = ['preco2', 'desconto', 'desconto_percentual']
colunas_selecionadas = st.multiselect(
    "📋 Selecione as informações para visualizar:",
    options=colunas_disponiveis,
    default=colunas_disponiveis
)

if not colunas_selecionadas:
    st.warning("Selecione pelo menos uma coluna para visualizar os dados.")
    st.stop()

# Faixa de preço categórica
bins = pd.cut(df_filtrado['preco2'], bins=5)
labels = [f"R${round(interval.left,2)} - R${round(interval.right,2)}" for interval in bins.cat.categories]
df_filtrado['faixa_preco'] = pd.cut(df_filtrado['preco2'], bins=5, labels=labels)

st.subheader("📄 Resumo Estatístico dos Dados Filtrados")
st.write(df_filtrado[colunas_selecionadas].describe())

st.subheader("📊 Gráficos Univariados")
col1, col2 = st.columns(2)

with col1:
    if 'preco2' in colunas_selecionadas:
        st.markdown("**Histograma de Preços**")
        fig1, ax1 = plt.subplots()
        sns.histplot(df_filtrado['preco2'], bins=20, ax=ax1, color='black')
        ax1.set_xlabel('Preço (R$)')
        st.pyplot(fig1)

with col2:
    if 'preco2' in colunas_selecionadas:
        st.markdown("**Boxplot de Preços**")
        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df_filtrado['preco2'], ax=ax2, color='pink')
        ax2.set_xlabel('Preço (R$)')
        st.pyplot(fig2)

st.subheader("📈 Gráficos Bivariados")
col3, col4 = st.columns(2)

with col3:
    if 'preco2' in colunas_selecionadas and 'desconto_percentual' in colunas_selecionadas:
        st.markdown("**Scatter Plot: Preço vs Desconto (%)**")
        fig3, ax3 = plt.subplots()
        sns.scatterplot(data=df_filtrado, x='preco2', y='desconto_percentual', ax=ax3, color='black')
        ax3.set_xlabel('Preço (R$)')
        ax3.set_ylabel('Desconto (%)')
        st.pyplot(fig3)

with col4:
    if 'desconto_percentual' in colunas_selecionadas:
        st.markdown("**Boxplot: Desconto por Faixa de Preço**")
        fig4, ax4 = plt.subplots()
        sns.boxplot(data=df_filtrado, x='faixa_preco', y='desconto_percentual', ax=ax4, palette='pink')
        ax4.set_xlabel('Faixa de Preço')
        ax4.set_ylabel('Desconto (%)')
        plt.xticks(rotation=45)
        st.pyplot(fig4)

st.subheader("💂️ Tabela de Dados Filtrados")
st.dataframe(df_filtrado[colunas_selecionadas])
