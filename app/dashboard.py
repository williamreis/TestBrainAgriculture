import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime
import os

# Configuração da página
st.set_page_config(
    page_title="TestBrainAgriculture Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurações - usar variável de ambiente ou fallback
API_BASE = os.getenv("API_BASE_URL", "http://api:8000")

def load_dashboard_data():
    """Carrega dados do dashboard da API"""
    try:
        response = requests.get(f"{API_BASE}/dashboard/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Erro ao carregar dados da API: {e}")
        return None

def main():
    # Header
    st.title("Dashboard")
    st.markdown("### Gerenciamento de Produtores Rurais")

    # Sidebar
    st.sidebar.title("Navegação")
    page = st.sidebar.selectbox(
        "Selecione a página:",
        ["Dashboard Geral", "Estatísticas Detalhadas"]
    )

    if page == "Dashboard Geral":
        show_main_dashboard()
    elif page == "Estatísticas Detalhadas":
        show_detailed_stats()


def show_main_dashboard():
    """Exibe o dashboard principal"""

    # Carregar dados
    with st.spinner("Carregando dados..."):
        data = load_dashboard_data()

    if not data:
        st.error("Não foi possível carregar os dados. Verifique se a API está rodando.")
        return

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total de Fazendas",
            value=data['estatisticas']['total_fazendas'],
            delta=None
        )

    with col2:
        st.metric(
            label="Total de Hectares",
            value=f"{data['estatisticas']['total_hectares']:,.0f} ha",
            delta=None
        )

    with col3:
        estados_count = len(data['grafico_estados'])
        st.metric(
            label="Estados Atendidos",
            value=estados_count,
            delta=None
        )

    with col4:
        culturas_count = len(data['grafico_culturas'])
        st.metric(
            label="Culturas Plantadas",
            value=culturas_count,
            delta=None
        )

    st.markdown("---")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico por Estado
        if data['grafico_estados']:
            df_estados = pd.DataFrame(data['grafico_estados'])
            fig_estados = px.pie(
                df_estados,
                values='quantidade',
                names='estado',
                title='Distribuição por Estado',
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_estados.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_estados, use_container_width=True)

        # Gráfico de Uso do Solo
        if data['grafico_uso_solo']:
            df_uso = pd.DataFrame(data['grafico_uso_solo'])
            fig_uso = px.pie(
                df_uso,
                values='area',
                names='tipo',
                title='Uso do Solo',
                color_discrete_sequence=['#2E8B57', '#228B22']
            )
            fig_uso.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_uso, use_container_width=True)

    with col2:
        # Gráfico por Cultura
        if data['grafico_culturas']:
            df_culturas = pd.DataFrame(data['grafico_culturas'])
            fig_culturas = px.bar(
                df_culturas,
                x='cultura',
                y='quantidade',
                title='Culturas Plantadas',
                color='quantidade',
                color_continuous_scale='viridis'
            )
            fig_culturas.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_culturas, use_container_width=True)

        # Gráfico de área por tipo
        if data['grafico_uso_solo']:
            df_uso = pd.DataFrame(data['grafico_uso_solo'])
            fig_area = px.bar(
                df_uso,
                x='tipo',
                y='area',
                title='Área por Tipo de Uso',
                color='tipo',
                color_discrete_sequence=['#2E8B57', '#228B22']
            )
            st.plotly_chart(fig_area, use_container_width=True)

def show_detailed_stats():
    """Exibe estatísticas detalhadas"""
    st.header("Estatísticas Detalhadas")

    data = load_dashboard_data()
    if not data:
        st.error("Não foi possível carregar os dados.")
        return

    # Tabelas detalhadas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Propriedades por Estado")
        if data['grafico_estados']:
            df_estados = pd.DataFrame(data['grafico_estados'])
            st.dataframe(
                df_estados.sort_values('quantidade', ascending=False),
                use_container_width=True
            )

    with col2:
        st.subheader("Culturas Plantadas")
        if data['grafico_culturas']:
            df_culturas = pd.DataFrame(data['grafico_culturas'])
            st.dataframe(
                df_culturas.sort_values('quantidade', ascending=False),
                use_container_width=True
            )

    # Gráfico de comparação
    if data['grafico_uso_solo']:
        st.subheader("Comparação de Áreas")
        df_uso = pd.DataFrame(data['grafico_uso_solo'])

        fig_comparison = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Área em Hectares', 'Percentual'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )

        # Bar chart
        fig_comparison.add_trace(
            go.Bar(x=df_uso['tipo'], y=df_uso['area'], name='Área (ha)'),
            row=1, col=1
        )

        # Pie chart
        fig_comparison.add_trace(
            go.Pie(labels=df_uso['tipo'], values=df_uso['percentual'], name='Percentual'),
            row=1, col=2
        )

        fig_comparison.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_comparison, use_container_width=True)


if __name__ == "__main__":
    main()