"""
Página de Coleta de Dados
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import time

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pipeline import PipelineColeta
from coletores.bitcoin import ColetorBitcoin
from coletores.ethereum import ColetorEthereum


def show():
    """Renderiza a página de coleta de dados"""

    st.header("⚡ Coleta de Dados")

    # Tabs para diferentes modos de coleta
    tab1, tab2, tab3 = st.tabs(["🚀 Coleta Manual", "⏰ Agendamento", "📋 Histórico"])

    with tab1:
        st.subheader("Executar Coleta Manual")

        col1, col2 = st.columns([3, 1])

        with col1:
            st.info("""
            **Como funciona:**
            - Executa a coleta de todos os ativos configurados
            - Salva automaticamente no banco de dados
            - Verifica alertas de variação
            - Envia notificações para Discord (se configurado)
            """)

        with col2:
            st.metric("Ativos", "2", "BTC, ETH")

        st.markdown("---")

        # Opções de coleta
        col1, col2 = st.columns(2)

        with col1:
            verificar_alertas = st.checkbox("Verificar alertas", value=True)
            if verificar_alertas:
                limite_variacao = st.slider(
                    "Limite de variação (%)",
                    min_value=1.0,
                    max_value=20.0,
                    value=3.0,
                    step=0.5
                )
            else:
                limite_variacao = 3.0

        with col2:
            enviar_discord = st.checkbox("Enviar para Discord", value=True)
            modo_detalhado = st.checkbox("Modo detalhado", value=False)

        st.markdown("---")

        # Botões de ação
        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            if st.button("▶️ Executar Pipeline Completo", type="primary", use_container_width=True):
                executar_pipeline_completo(verificar_alertas, limite_variacao, modo_detalhado)

        with col2:
            if st.button("₿ Coletar apenas Bitcoin", use_container_width=True):
                executar_coletor_individual("Bitcoin", ColetorBitcoin())

        with col3:
            if st.button("Ξ Coletar apenas Ethereum", use_container_width=True):
                executar_coletor_individual("Ethereum", ColetorEthereum())

    with tab2:
        st.subheader("⏰ Agendamento Automático")

        st.warning("""
        ⚠️ **Atenção:** O agendamento automático deve ser executado via terminal para rodar em background.
        Esta interface permite apenas configurar e iniciar, mas não mantém o processo ativo.
        """)

        col1, col2 = st.columns(2)

        with col1:
            intervalo = st.selectbox(
                "Intervalo de coleta:",
                [5, 15, 30, 60, 360],
                index=2,
                format_func=lambda x: f"{x} minutos"
            )

        with col2:
            st.metric("Próxima execução", "N/A", "Não agendado")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶️ Iniciar Agendamento", type="primary", use_container_width=True):
                st.info(f"""
                Para iniciar o agendamento, execute no terminal:

                ```bash
                ./run_service.sh start
                ```

                Ou manualmente:

                ```bash
                .venv/bin/python3 src/scheduler.py
                ```
                """)

        with col2:
            if st.button("⏹️ Parar Agendamento", use_container_width=True):
                st.info("""
                Para parar o agendamento, execute no terminal:

                ```bash
                ./run_service.sh stop
                ```
                """)

        st.markdown("---")

        # Status do serviço
        st.subheader("📊 Status do Serviço")

        import os
        if os.path.exists('pipeline.pid'):
            with open('pipeline.pid', 'r') as f:
                pid = f.read().strip()

            st.success(f"✅ Serviço está rodando (PID: {pid})")

            # Tentar ler últimas linhas do log
            if os.path.exists('logs/service.log'):
                with open('logs/service.log', 'r') as f:
                    lines = f.readlines()
                    ultimas_linhas = ''.join(lines[-20:])

                with st.expander("Ver logs recentes"):
                    st.code(ultimas_linhas, language='text')
        else:
            st.info("ℹ️ Serviço não está rodando")

    with tab3:
        st.subheader("📋 Histórico de Coletas")

        from database.db_manager import DatabaseManager

        try:
            db = DatabaseManager()
            ativos = db.listar_ativos()

            if ativos:
                # Seletor de ativo
                ativo_selecionado = st.selectbox(
                    "Ativo:",
                    [a['ativo'] for a in ativos]
                )

                # Quantidade de registros
                limite = st.slider("Registros a exibir:", 5, 100, 20)

                historico = db.obter_historico(ativo_selecionado, limite)

                if historico:
                    import pandas as pd

                    df = pd.DataFrame(historico)
                    df = df.sort_values('id', ascending=False)

                    # Adicionar coluna de variação
                    if len(df) > 1:
                        df['variacao'] = df['preco'].pct_change(-1) * 100
                        df['variacao'] = df['variacao'].fillna(0)

                    # Formatar para exibição
                    df_display = df[['horario_coleta', 'preco', 'moeda', 'variacao']].copy()
                    df_display.columns = ['Data/Hora', 'Preço', 'Moeda', 'Variação (%)']

                    st.dataframe(
                        df_display.style.format({
                            'Preço': '${:,.2f}',
                            'Variação (%)': '{:+.2f}%'
                        }).applymap(
                            lambda x: 'color: green' if isinstance(x, (int, float)) and x > 0 else ('color: red' if isinstance(x, (int, float)) and x < 0 else ''),
                            subset=['Variação (%)']
                        ),
                        use_container_width=True,
                        hide_index=True
                    )

                    # Estatísticas rápidas
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Registros", len(df))

                    with col2:
                        st.metric("Último Preço", f"${df['preco'].iloc[0]:,.2f}")

                    with col3:
                        if len(df) > 1:
                            diff = df['preco'].iloc[0] - df['preco'].iloc[-1]
                            st.metric("Variação Total", f"${diff:+,.2f}")

                    with col4:
                        st.metric("Coletas/dia", f"{len(df) / 7:.1f}")

                else:
                    st.info("Nenhum histórico encontrado.")
            else:
                st.warning("Nenhum ativo disponível. Execute uma coleta primeiro!")

        except Exception as e:
            st.error(f"Erro ao carregar histórico: {e}")


def executar_pipeline_completo(verificar_alertas, limite_variacao, modo_detalhado):
    """Executa o pipeline completo"""

    with st.status("Executando pipeline...", expanded=True) as status:
        try:
            st.write("🚀 Iniciando pipeline...")
            time.sleep(0.5)

            # Criar pipeline
            pipeline = PipelineColeta(
                habilitar_alertas=verificar_alertas,
                limite_variacao=limite_variacao
            )

            st.write("📡 Coletando dados...")
            resultados = pipeline.executar()

            st.write("✅ Pipeline concluído!")

            status.update(label="Pipeline executado com sucesso!", state="complete")

            # Mostrar resultados
            st.success("✅ Coleta concluída com sucesso!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("✅ Sucessos", len(resultados['sucesso']))

            with col2:
                st.metric("❌ Falhas", len(resultados['falha']))

            with col3:
                taxa_sucesso = (len(resultados['sucesso']) / resultados['total']) * 100 if resultados['total'] > 0 else 0
                st.metric("Taxa de Sucesso", f"{taxa_sucesso:.1f}%")

            if resultados['sucesso']:
                st.info(f"Ativos coletados: {', '.join(resultados['sucesso'])}")

            if resultados['falha']:
                st.warning(f"Falhas em: {', '.join(resultados['falha'])}")

        except Exception as e:
            status.update(label="Erro na execução!", state="error")
            st.error(f"❌ Erro ao executar pipeline: {e}")


def executar_coletor_individual(nome, coletor):
    """Executa um coletor individual"""

    with st.status(f"Coletando {nome}...", expanded=True) as status:
        try:
            st.write(f"📡 Conectando à API de {nome}...")
            time.sleep(0.5)

            sucesso = coletor.executar()

            if sucesso:
                status.update(label=f"{nome} coletado com sucesso!", state="complete")
                st.success(f"✅ {nome} coletado e salvo com sucesso!")

                # Mostrar último preço
                from database.db_manager import DatabaseManager
                db = DatabaseManager()
                ultimo = db.obter_ultimo_preco(coletor.nome_ativo)

                if ultimo:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Preço", f"${ultimo['preco']:,.2f}")

                    with col2:
                        st.metric("Horário", ultimo['horario_coleta'].split()[1][:5])
            else:
                status.update(label=f"Erro ao coletar {nome}", state="error")
                st.error(f"❌ Erro ao coletar {nome}")

        except Exception as e:
            status.update(label=f"Erro na coleta de {nome}", state="error")
            st.error(f"❌ Erro: {e}")
