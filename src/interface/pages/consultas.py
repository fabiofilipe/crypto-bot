"""
Página de Consultas e Análises
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.db_manager import DatabaseManager


@st.cache_resource
def _get_db():
    """Cache do DatabaseManager (connection pooling)"""
    return DatabaseManager()


def show():
    """Renderiza a página de consultas"""

    st.header("🔍 Consultas e Análises")

    db = _get_db()

    # Tabs para diferentes consultas
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Estatísticas", "📜 Histórico", "🔄 Comparação", "💾 Exportação"])

    with tab1:
        st.subheader("📊 Estatísticas dos Ativos")

        ativos = db.listar_ativos()

        if not ativos:
            st.warning("Nenhum ativo disponível. Execute uma coleta primeiro!")
            return

        # Seletor de ativo
        col1, col2 = st.columns([2, 1])

        with col1:
            ativo_selecionado = st.selectbox(
                "Selecione o ativo:",
                [a['ativo'] for a in ativos]
            )

        with col2:
            dias = st.selectbox(
                "Período:",
                [1, 7, 15, 30, 90],
                index=1,
                format_func=lambda x: f"{x} dia(s)"
            )

        # Buscar estatísticas
        stats = db.obter_estatisticas(ativo_selecionado, dias)
        ultimo = db.obter_ultimo_preco(ativo_selecionado)

        if stats and ultimo:
            st.markdown("---")

            # Métricas principais
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.metric(
                    "💰 Preço Atual",
                    f"${ultimo['preco']:,.2f}",
                    delta=f"{ultimo['moeda']}"
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
                    f"{variacao:.2f}%"
                )

            st.markdown("---")

            # Informações detalhadas
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📅 Período Analisado")
                st.info(f"""
                **Primeira Coleta:** {stats['primeira_coleta']}

                **Última Coleta:** {stats['ultima_coleta']}

                **Total de Registros:** {stats['total_registros']:,}

                **Coletas/dia:** {stats['total_registros'] / dias:.1f}
                """)

            with col2:
                st.markdown("### 💹 Análise de Preços")

                amplitude = stats['preco_maximo'] - stats['preco_minimo']
                diff_atual_media = ultimo['preco'] - stats['preco_medio']
                perc_media = (diff_atual_media / stats['preco_medio']) * 100

                st.info(f"""
                **Amplitude:** ${amplitude:,.2f}

                **Diferença da Média:** ${diff_atual_media:+,.2f} ({perc_media:+.2f}%)

                **Status:** {'Acima da média' if diff_atual_media > 0 else 'Abaixo da média'}

                **Volatilidade:** {'Alta' if variacao > 10 else 'Média' if variacao > 5 else 'Baixa'}
                """)

        else:
            st.warning("Nenhum dado disponível para o período selecionado.")

    with tab2:
        st.subheader("📜 Histórico Detalhado")

        ativos = db.listar_ativos()

        if ativos:
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                ativo_selecionado = st.selectbox(
                    "Ativo:",
                    [a['ativo'] for a in ativos],
                    key="hist_ativo"
                )

            with col2:
                limite = st.number_input(
                    "Registros:",
                    min_value=5,
                    max_value=1000,
                    value=50,
                    step=5
                )

            with col3:
                ordem = st.selectbox(
                    "Ordenar:",
                    ["Mais recente", "Mais antigo"]
                )

            # Buscar histórico
            historico = db.obter_historico(ativo_selecionado, limite)

            if historico:
                df = pd.DataFrame(historico)

                # Ordenar
                if ordem == "Mais antigo":
                    df = df.sort_values('id', ascending=True)
                else:
                    df = df.sort_values('id', ascending=False)

                # Calcular variações
                df['variacao'] = df['preco'].pct_change(-1) * 100
                df['variacao'] = df['variacao'].fillna(0)

                # Adicionar coluna de tendência
                df['tendencia'] = df['variacao'].apply(
                    lambda x: '📈' if x > 0 else ('📉' if x < 0 else '➡️')
                )

                # Preparar para exibição
                df_display = df[['horario_coleta', 'preco', 'moeda', 'variacao', 'tendencia']].copy()
                df_display.columns = ['Data/Hora', 'Preço', 'Moeda', 'Variação (%)', 'Tendência']

                # Exibir tabela
                st.dataframe(
                    df_display.style.format({
                        'Preço': '${:,.2f}',
                        'Variação (%)': '{:+.2f}%'
                    }).applymap(
                        lambda x: 'background-color: #d4edda' if isinstance(x, (int, float)) and x > 0 else (
                            'background-color: #f8d7da' if isinstance(x, (int, float)) and x < 0 else ''),
                        subset=['Variação (%)']
                    ),
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )

                # Estatísticas do período exibido
                st.markdown("---")
                st.subheader("📊 Estatísticas do Período Exibido")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Registros", len(df))

                with col2:
                    st.metric("Preço Médio", f"${df['preco'].mean():,.2f}")

                with col3:
                    variacao_total = ((df['preco'].iloc[0] - df['preco'].iloc[-1]) / df['preco'].iloc[-1]) * 100
                    st.metric("Variação Total", f"{variacao_total:+.2f}%")

                with col4:
                    st.metric("Desvio Padrão", f"${df['preco'].std():,.2f}")

            else:
                st.info("Nenhum histórico encontrado.")
        else:
            st.warning("Nenhum ativo disponível.")

    with tab3:
        st.subheader("🔄 Comparação entre Ativos")

        ativos = db.listar_ativos()

        if len(ativos) < 2:
            st.warning("É necessário ter pelo menos 2 ativos para comparação.")
            return

        # Seleção de ativos
        col1, col2 = st.columns([3, 1])

        with col1:
            ativos_comparar = st.multiselect(
                "Selecione ativos para comparar:",
                [a['ativo'] for a in ativos],
                default=[a['ativo'] for a in ativos[:2]]
            )

        with col2:
            dias_comp = st.selectbox(
                "Período:",
                [1, 7, 15, 30],
                index=1,
                format_func=lambda x: f"{x} dia(s)",
                key="comp_dias"
            )

        if len(ativos_comparar) >= 2:
            st.markdown("---")

            # Tabela comparativa
            comparacao_data = []

            for ativo in ativos_comparar:
                ultimo = db.obter_ultimo_preco(ativo)
                stats = db.obter_estatisticas(ativo, dias_comp)

                if ultimo and stats:
                    variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

                    comparacao_data.append({
                        'Ativo': ativo,
                        'Preço Atual': f"${ultimo['preco']:,.2f}",
                        'Mínimo': f"${stats['preco_minimo']:,.2f}",
                        'Médio': f"${stats['preco_medio']:,.2f}",
                        'Máximo': f"${stats['preco_maximo']:,.2f}",
                        'Variação': f"{variacao:.2f}%",
                        'Registros': stats['total_registros']
                    })

            if comparacao_data:
                df_comp = pd.DataFrame(comparacao_data)
                st.dataframe(df_comp, use_container_width=True, hide_index=True)

                # Análise comparativa
                st.markdown("---")
                st.subheader("📈 Análise Comparativa")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Maiores Variações")
                    df_temp = df_comp.copy()
                    df_temp['Variação_num'] = df_temp['Variação'].str.replace('%', '').astype(float)
                    df_sorted = df_temp.sort_values('Variação_num', ascending=False)

                    for idx, row in df_sorted.iterrows():
                        emoji = "📈" if float(row['Variação_num']) > 0 else "📉"
                        st.info(f"{emoji} **{row['Ativo']}**: {row['Variação']}")

                with col2:
                    st.markdown("#### Mais Coletados")
                    df_sorted_reg = df_comp.sort_values('Registros', ascending=False)

                    for idx, row in df_sorted_reg.iterrows():
                        st.info(f"📊 **{row['Ativo']}**: {row['Registros']} registros")

        else:
            st.info("Selecione pelo menos 2 ativos para comparar.")

    with tab4:
        st.subheader("💾 Exportação de Dados")

        ativos = db.listar_ativos()

        if ativos:
            col1, col2 = st.columns([2, 1])

            with col1:
                ativo_export = st.selectbox(
                    "Ativo para exportar:",
                    [a['ativo'] for a in ativos],
                    key="export_ativo"
                )

            with col2:
                limite_export = st.number_input(
                    "Máximo de registros:",
                    min_value=10,
                    max_value=10000,
                    value=1000,
                    step=100
                )

            formato = st.radio(
                "Formato de exportação:",
                ["CSV", "JSON", "Excel"],
                horizontal=True
            )

            st.markdown("---")

            if st.button("📥 Exportar Dados", type="primary"):
                with st.spinner("Exportando dados..."):
                    try:
                        historico = db.obter_historico(ativo_export, limite_export)

                        if historico:
                            df = pd.DataFrame(historico)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                            if formato == "CSV":
                                filename = f"data/exportacao_{ativo_export.lower()}_{timestamp}.csv"
                                df.to_csv(filename, index=False)
                                st.success(f"✅ Exportado: {filename}")

                                # Botão para download
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="⬇️ Baixar CSV",
                                    data=csv,
                                    file_name=f"{ativo_export}_{timestamp}.csv",
                                    mime="text/csv"
                                )

                            elif formato == "JSON":
                                filename = f"data/exportacao_{ativo_export.lower()}_{timestamp}.json"
                                df.to_json(filename, orient='records', indent=2)
                                st.success(f"✅ Exportado: {filename}")

                                # Botão para download
                                json_str = df.to_json(orient='records', indent=2)
                                st.download_button(
                                    label="⬇️ Baixar JSON",
                                    data=json_str,
                                    file_name=f"{ativo_export}_{timestamp}.json",
                                    mime="application/json"
                                )

                            elif formato == "Excel":
                                filename = f"data/exportacao_{ativo_export.lower()}_{timestamp}.xlsx"
                                df.to_excel(filename, index=False)
                                st.success(f"✅ Exportado: {filename}")

                                # Nota sobre download do Excel
                                st.info("📁 Arquivo Excel salvo localmente. Para baixar, acesse a pasta `data/`")

                            # Mostrar preview
                            with st.expander("👁️ Preview dos dados exportados"):
                                st.dataframe(df.head(10), use_container_width=True)

                            st.info(f"📊 Total de {len(df):,} registros exportados")

                        else:
                            st.warning("Nenhum dado disponível para exportar.")

                    except Exception as e:
                        st.error(f"Erro ao exportar: {e}")
        else:
            st.warning("Nenhum ativo disponível para exportação.")

        # Histórico de exportações
        st.markdown("---")
        st.subheader("📂 Exportações Anteriores")

        import os
        data_dir = Path("data")

        if data_dir.exists():
            exportacoes = list(data_dir.glob("exportacao_*"))

            if exportacoes:
                for arquivo in sorted(exportacoes, reverse=True)[:10]:
                    st.text(f"📄 {arquivo.name} ({arquivo.stat().st_size / 1024:.1f} KB)")
            else:
                st.info("Nenhuma exportação anterior encontrada.")
        else:
            st.info("Diretório de exportações não encontrado.")
