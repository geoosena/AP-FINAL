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

# Limpeza e tratamento
df['preco2'] = df['preco2'].astype(str).str.replace('R\$', '', regex=True).str.replace(',', '.').astype(float)
df['desconto'] = df['desconto'].fillna('0').astype(str)
df['desconto'] = df['desconto'].str.replace('%', '', regex=True).str.replace('-', '0').str.strip()
df['desconto'] = pd.to_numeric(df['desconto'], errors='coerce').fillna(0)

# Cálculo do percentual de desconto
df['desconto_percentual'] = (df['desconto'] / (df['preco2'] + df['desconto'])) * 100

# 🚨 Alerta se tudo estiver zerado
if df['desconto_percentual'].sum() == 0:
    st.warning("🚨 Atenção: Todos os valores de 'desconto_percentual' estão zerados. Verifique se os dados foram carregados corretamente e se o cálculo está adequado.")

# Faixa de preço filtrável
preco_min, preco_max = df['preco2'].min(), df['preco2'].max()
preco_range = st.slider(
    "🔎 Filtrar por faixa de preço (R$):", 
    min_value=float(preco_min), 
    max_value=float(preco_max), 
    value=(float(preco_min), float(preco_max))
)

df_filtrado = df[(df['preco2'] >= preco_range[0]) & (df['preco2'] <= preco_range[1])]

# Faixas categóricas para boxplot
bins = pd.cut(df_filtrado['preco2'], bins=5)
labels = [f"R${round(interval.left,2)} - R${round(interval.right,2)}" for interval in bins.cat.categories]
df_filtrado['faixa_preco'] = pd.cut(df_filtrado['preco2'], bins=5, labels=labels)

# Resumo estatístico
st.subheader("📄 Resumo Estatístico dos Dados Filtrados")
st.write(df_filtrado[['preco2', 'desconto', 'desconto_percentual']].describe())

# Gráficos univariados
variaveis_numericas = ['preco2', 'desconto', 'desconto_percentual']

st.subheader("📊 Gráficos Univariados")
col1, col2 = st.columns(2)

with col1:
    var_hist = st.selectbox("Variável para o Histograma:", variaveis_numericas, index=0)
    st.markdown(f"**Histograma de {var_hist}**")
    fig1, ax1 = plt.subplots()
    sns.histplot(df_filtrado[var_hist], bins=20, ax=ax1, color='black')
    ax1.set_xlabel(var_hist)
    st.pyplot(fig1)

with col2:
    var_box = st.selectbox("Variável para o Boxplot:", variaveis_numericas, index=0)
    st.markdown(f"**Boxplot de {var_box}**")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x=df_filtrado[var_box], ax=ax2, color='pink')
    ax2.set_xlabel(var_box)
    st.pyplot(fig2)

# Gráficos bivariados
st.subheader("📈 Gráficos Bivariados")
col3, col4 = st.columns(2)

with col3:
    x_scatter = st.selectbox("Eixo X (scatter):", variaveis_numericas, index=0)
    y_scatter = st.selectbox("Eixo Y (scatter):", variaveis_numericas, index=2)
    st.markdown(f"**Scatter Plot: {x_scatter} vs {y_scatter}**")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(data=df_filtrado, x=x_scatter, y=y_scatter, ax=ax3, color='black')
    ax3.set_xlabel(x_scatter)
    ax3.set_ylabel(y_scatter)
    st.pyplot(fig3)

with col4:
    st.markdown("**Boxplot: Desconto por Faixa de Preço**")
    fig4, ax4 = plt.subplots()
    sns.boxplot(data=df_filtrado, x='faixa_preco', y='desconto_percentual', ax=ax4, palette='pink')
    ax4.set_xlabel('Faixa de Preço')
    ax4.set_ylabel('Desconto (%)')
    plt.xticks(rotation=45)
    st.pyplot(fig4)

# Tabela com dados filtrados
st.subheader("💂️ Tabela de Dados Filtrados")
st.dataframe(df_filtrado)
