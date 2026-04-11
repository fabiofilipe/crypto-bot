"""
Página de Dashboard com gráficos
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.db_manager import DatabaseManager


@st.cache_resource
def _get_db():
    """Cache do DatabaseManager (connection pooling)"""
    return DatabaseManager()


def show():
    """Renderiza a página de dashboard"""

    st.header("📊 Dashboard de Monitoramento")

    db = _get_db()

    # Controles
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        ativos = db.listar_ativos()
        if not ativos:
            st.warning("⚠️ Nenhum dado disponível. Execute uma coleta primeiro!")
            return

        ativos_disponiveis = [a['ativo'] for a in ativos]
        ativo_selecionado = st.selectbox(
            "Selecione o ativo:",
            ativos_disponiveis
        )

    with col2:
        periodo = st.selectbox(
            "Período:",
            ["Últimas 24h", "Últimos 7 dias", "Últimos 30 dias", "Tudo"],
            index=1
        )

    with col3:
        auto_refresh = st.checkbox("Auto-refresh", value=False)

    if auto_refresh:
        st.rerun()

    st.markdown("---")

    # Calcular dias baseado no período
    dias_map = {
        "Últimas 24h": 1,
        "Últimos 7 dias": 7,
        "Últimos 30 dias": 30,
        "Tudo": 999999
    }
    dias = dias_map[periodo]

    # Métricas principais
    try:
        ultimo = db.obter_ultimo_preco(ativo_selecionado)
        stats = db.obter_estatisticas(ativo_selecionado, dias)

        if ultimo and stats:
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric(
                    "💰 Preço Atual",
                    f"${ultimo['preco']:,.2f}",
                    f"{ultimo['moeda']}"
                )

            with col2:
                st.metric(
                    "📉 Mínimo",
                    f"${stats['preco_minimo']:,.2f}"
                )

            with col3:
                st.metric(
                    "📊 Médio",
                    f"${stats['preco_medio']:,.2f}"
                )

            with col4:
                st.metric(
                    "📈 Máximo",
                    f"${stats['preco_maximo']:,.2f}"
                )

            with col5:
                variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100
                st.metric(
                    "📊 Variação",
                    f"{variacao:.2f}%",
                    delta=f"{variacao:.2f}%"
                )

    except Exception as e:
        st.error(f"Erro ao carregar métricas: {e}")

    st.markdown("---")

    # Gráficos
    tab1, tab2, tab3 = st.tabs(["📈 Linha do Tempo", "📊 Estatísticas", "🔍 Análise Detalhada"])

    with tab1:
        try:
            # Buscar histórico
            historico = db.obter_historico(ativo_selecionado, limite=1000)

            if historico:
                df = pd.DataFrame(historico)
                df['horario_coleta'] = pd.to_datetime(df['horario_coleta'])

                # Filtrar por período
                if periodo != "Tudo":
                    data_limite = datetime.now() - timedelta(days=dias)
                    df = df[df['horario_coleta'] >= data_limite]

                # Gráfico de linha
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df['horario_coleta'],
                    y=df['preco'],
                    mode='lines+markers',
                    name=ativo_selecionado,
                    line=dict(color='#1f77b4', width=2),
                    marker=dict(size=4),
                    hovertemplate='<b>%{x}</b><br>Preço: $%{y:,.2f}<extra></extra>'
                ))

                fig.update_layout(
                    title=f'Evolução do Preço - {ativo_selecionado}',
                    xaxis_title='Data/Hora',
                    yaxis_title=f'Preço ({ultimo["moeda"]})',
                    hovermode='x unified',
                    height=500,
                    template='plotly_white'
                )

                st.plotly_chart(fig, use_container_width=True)

                # Estatísticas rápidas
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.info(f"📊 **Registros:** {len(df)}")

                with col2:
                    if len(df) > 1:
                        diff = df['preco'].iloc[0] - df['preco'].iloc[-1]
                        perc = (diff / df['preco'].iloc[-1]) * 100
                        st.info(f"📈 **Mudança:** {diff:+,.2f} ({perc:+.2f}%)")

                with col3:
                    std = df['preco'].std()
                    st.info(f"📊 **Volatilidade:** ${std:,.2f}")

            else:
                st.warning("Nenhum dado disponível para o período selecionado.")

        except Exception as e:
            st.error(f"Erro ao gerar gráfico: {e}")

    with tab2:
        try:
            historico = db.obter_historico(ativo_selecionado, limite=1000)

            if historico:
                df = pd.DataFrame(historico)
                df['horario_coleta'] = pd.to_datetime(df['horario_coleta'])

                # Filtrar por período
                if periodo != "Tudo":
                    data_limite = datetime.now() - timedelta(days=dias)
                    df = df[df['horario_coleta'] >= data_limite]

                col1, col2 = st.columns(2)

                with col1:
                    # Histograma de preços
                    fig_hist = px.histogram(
                        df,
                        x='preco',
                        nbins=30,
                        title='Distribuição de Preços',
                        labels={'preco': f'Preço ({ultimo["moeda"]})', 'count': 'Frequência'}
                    )
                    fig_hist.update_layout(height=400)
                    st.plotly_chart(fig_hist, use_container_width=True)

                with col2:
                    # Box plot
                    fig_box = px.box(
                        df,
                        y='preco',
                        title='Box Plot - Análise de Dispersão',
                        labels={'preco': f'Preço ({ultimo["moeda"]})'}
                    )
                    fig_box.update_layout(height=400)
                    st.plotly_chart(fig_box, use_container_width=True)

                # Estatísticas descritivas
                st.subheader("📊 Estatísticas Descritivas")

                stats_df = pd.DataFrame({
                    'Métrica': ['Contagem', 'Média', 'Mediana', 'Desvio Padrão', 'Mínimo', 'Máximo', 'Amplitude'],
                    'Valor': [
                        f"{len(df):,}",
                        f"${df['preco'].mean():,.2f}",
                        f"${df['preco'].median():,.2f}",
                        f"${df['preco'].std():,.2f}",
                        f"${df['preco'].min():,.2f}",
                        f"${df['preco'].max():,.2f}",
                        f"${df['preco'].max() - df['preco'].min():,.2f}"
                    ]
                })

                st.dataframe(stats_df, use_container_width=True, hide_index=True)

            else:
                st.warning("Nenhum dado disponível para análise.")

        except Exception as e:
            st.error(f"Erro ao gerar estatísticas: {e}")

    with tab3:
        try:
            historico = db.obter_historico(ativo_selecionado, limite=1000)

            if historico:
                df = pd.DataFrame(historico)
                df['horario_coleta'] = pd.to_datetime(df['horario_coleta'])

                # Filtrar por período
                if periodo != "Tudo":
                    data_limite = datetime.now() - timedelta(days=dias)
                    df = df[df['horario_coleta'] >= data_limite]

                # Adicionar coluna de data
                df['data'] = df['horario_coleta'].dt.date

                # Gráfico de candlestick por dia
                daily_stats = df.groupby('data').agg({
                    'preco': ['first', 'max', 'min', 'last', 'count']
                }).reset_index()

                daily_stats.columns = ['data', 'open', 'high', 'low', 'close', 'count']

                fig_candle = go.Figure(data=[go.Candlestick(
                    x=daily_stats['data'],
                    open=daily_stats['open'],
                    high=daily_stats['high'],
                    low=daily_stats['low'],
                    close=daily_stats['close'],
                    name=ativo_selecionado
                )])

                fig_candle.update_layout(
                    title=f'Candlestick - {ativo_selecionado}',
                    xaxis_title='Data',
                    yaxis_title=f'Preço ({ultimo["moeda"]})',
                    height=500,
                    template='plotly_white'
                )

                st.plotly_chart(fig_candle, use_container_width=True)

                # Tabela de dados diários
                st.subheader("📅 Resumo Diário")

                daily_display = daily_stats.copy()
                daily_display['variacao'] = ((daily_display['close'] - daily_display['open']) / daily_display['open'] * 100).round(2)
                daily_display = daily_display.sort_values('data', ascending=False).head(10)

                st.dataframe(
                    daily_display.style.format({
                        'open': '${:,.2f}',
                        'high': '${:,.2f}',
                        'low': '${:,.2f}',
                        'close': '${:,.2f}',
                        'variacao': '{:+.2f}%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.warning("Nenhum dado disponível para análise detalhada.")

        except Exception as e:
            st.error(f"Erro ao gerar análise: {e}")

    # Comparação entre ativos
    st.markdown("---")
    st.subheader("🔄 Comparação entre Ativos")

    if len(ativos_disponiveis) > 1:
        ativos_comparar = st.multiselect(
            "Selecione ativos para comparar:",
            ativos_disponiveis,
            default=ativos_disponiveis[:2] if len(ativos_disponiveis) >= 2 else ativos_disponiveis
        )

        if len(ativos_comparar) >= 2:
            fig_comp = go.Figure()

            for ativo in ativos_comparar:
                historico = db.obter_historico(ativo, limite=1000)
                if historico:
                    df = pd.DataFrame(historico)
                    df['horario_coleta'] = pd.to_datetime(df['horario_coleta'])

                    if periodo != "Tudo":
                        data_limite = datetime.now() - timedelta(days=dias)
                        df = df[df['horario_coleta'] >= data_limite]

                    # Normalizar para comparação (base 100)
                    df['preco_norm'] = (df['preco'] / df['preco'].iloc[-1]) * 100

                    fig_comp.add_trace(go.Scatter(
                        x=df['horario_coleta'],
                        y=df['preco_norm'],
                        mode='lines',
                        name=ativo,
                        hovertemplate=f'<b>{ativo}</b><br>%{{x}}<br>Índice: %{{y:.2f}}<extra></extra>'
                    ))

            fig_comp.update_layout(
                title='Comparação Normalizada (Base 100)',
                xaxis_title='Data/Hora',
                yaxis_title='Índice (Base 100)',
                hovermode='x unified',
                height=400,
                template='plotly_white'
            )

            st.plotly_chart(fig_comp, use_container_width=True)

            # Tabela comparativa
            col1, col2 = st.columns(2)

            for idx, ativo in enumerate(ativos_comparar):
                stats = db.obter_estatisticas(ativo, dias)
                ultimo = db.obter_ultimo_preco(ativo)

                if stats and ultimo:
                    with col1 if idx % 2 == 0 else col2:
                        variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

                        st.info(f"""
                        **{ativo}**
                        - Atual: ${ultimo['preco']:,.2f}
                        - Média: ${stats['preco_medio']:,.2f}
                        - Variação: {variacao:.2f}%
                        """)
