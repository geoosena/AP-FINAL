import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


caminho_dados = os.path.join('..', 'Bases tratadas', 'dados_shein_tratado.csv')


df = pd.read_csv(caminho_dados, sep=';')

st.set_page_config(layout="wide")
st.title("Análise de Produtos da Shein")
st.markdown("Aplicação interativa para explorar preços e descontos de produtos da Shein.")


preco_min, preco_max = float(df['preco2'].min()), float(df['preco2'].max())
preco_range = st.slider("Filtrar por faixa de preço (R$)", min_value=preco_min, max_value=preco_max, value=(preco_min, preco_max))

df_filtrado = df[(df['preco2'] >= preco_range[0]) & (df['preco2'] <= preco_range[1])]


st.subheader("Resumo estatístico dos dados filtrados:")
st.write(df_filtrado[['preco2']].describe())

st.subheader("Gráficos Univariados")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Histograma de Preços**")
fig1, ax1 = plt.subplots()
sns.histplot(df_filtrado['preco2'], bins=20, ax=ax1)
st.pyplot(fig1)

with col2:
    st.markdown("**Boxplot de Preços**")
fig2, ax2 = plt.subplots()
sns.boxplot(x=df_filtrado['preco2'], ax=ax2)
st.pyplot(fig2)


st.subheader("Gráficos Bivariados")


df_filtrado['desconto_num'] = df_filtrado['desconto'].str.replace('%', '').str.strip()
df_filtrado['desconto_num'] = pd.to_numeric(df_filtrado['desconto_num'], errors='coerce')

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Scatter Plot: Preço vs Desconto (%)**")
fig3, ax3 = plt.subplots()
sns.scatterplot(data=df_filtrado, x='preco2', y='desconto_num', ax=ax3)
st.pyplot(fig3)

with col4:
    st.markdown("**Boxplot: Desconto por Faixa de Preço**")
df_filtrado['faixa_preco'] = pd.cut(df_filtrado['preco2'], bins=5)
fig4, ax4 = plt.subplots()
sns.boxplot(data=df_filtrado, x='faixa_preco', y='desconto_num', ax=ax4)
plt.xticks(rotation=45)
st.pyplot(fig4)