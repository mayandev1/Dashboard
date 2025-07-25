import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard Supermercado", page_icon="🛒")

# Carregando os dados
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# Criando coluna "Month"
df["Month"] = df["Date"].dt.to_period("M").astype(str)

# Sidebar
st.sidebar.title("🔍 Filtros")
month = st.sidebar.selectbox("Selecione o mês", df["Month"].unique())

# Filtrando os dados
df_filtered = df[df["Month"] == month]

# Título principal
st.markdown("## 📊 Visão Geral de Vendas")
st.markdown(f"### Mês selecionado: `{month}`")

# Gráficos principais
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Faturamento por dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="📅 Faturamento por Dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Faturamento por tipo de produto
fig_prod = px.bar(df_filtered, x="Product line", y="Total", 
                  color="City", title="🧾 Faturamento por Tipo de Produto",
                  barmode="group")
col2.plotly_chart(fig_prod, use_container_width=True)

# Faturamento por filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="🏢 Faturamento por Filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", title="💳 Tipo de Pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Avaliação média por filial
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_rating, x="City", y="Rating", title="⭐ Avaliação Média por Filial")
col5.plotly_chart(fig_rating, use_container_width=True)

# Novos gráficos extras
st.markdown("## 📈 Insights Extras")
col6, col7 = st.columns(2)

# Faturamento acumulado por cidade (linha)
fig_cum = px.line(df_filtered.groupby(["Date", "City"])["Total"].sum().reset_index(),
                  x="Date", y="Total", color="City", title="📈 Faturamento Acumulado por Cidade")
col6.plotly_chart(fig_cum, use_container_width=True)

# Média de vendas por tipo de produto
avg_product = df_filtered.groupby("Product line")["Total"].mean().reset_index()
fig_avg_prod = px.bar(avg_product, x="Product line", y="Total", title="📦 Média de Faturamento por Tipo de Produto")
col7.plotly_chart(fig_avg_prod, use_container_width=True)
