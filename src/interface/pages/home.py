"""
Página inicial da interface
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from database.db_manager import DatabaseManager


def show():
    """Renderiza a página inicial"""

    st.header("🏠 Bem-vindo ao Sistema de Coleta Financeira")

    # Cards de informação
    col1, col2, col3 = st.columns(3)

    try:
        db = DatabaseManager()
        ativos = db.listar_ativos()

        # Card 1: Total de ativos
        with col1:
            st.metric(
                label="📈 Ativos Monitorados",
                value=len(ativos),
                delta="Ativos ativos"
            )

        # Card 2: Total de registros
        total_registros = sum(a['total_registros'] for a in ativos)
        with col2:
            st.metric(
                label="📊 Total de Registros",
                value=f"{total_registros:,}",
                delta="Coletas realizadas"
            )

        # Card 3: Última atualização
        with col3:
            if ativos:
                ultimo_preco = db.obter_ultimo_preco(ativos[0]['ativo'])
                if ultimo_preco:
                    st.metric(
                        label="🕐 Última Coleta",
                        value=ultimo_preco['horario_coleta'].split()[1][:5],
                        delta=ultimo_preco['horario_coleta'].split()[0]
                    )
            else:
                st.metric(
                    label="🕐 Última Coleta",
                    value="N/A",
                    delta="Nenhuma coleta ainda"
                )

    except Exception as e:
        st.error(f"Erro ao carregar estatísticas: {e}")

    st.markdown("---")

    # Visão geral dos ativos
    st.subheader("📊 Visão Geral dos Ativos")

    if ativos:
        for ativo_info in ativos:
            with st.expander(f"{ativo_info['ativo']} - {ativo_info['total_registros']} registros"):
                try:
                    ultimo = db.obter_ultimo_preco(ativo_info['ativo'])
                    stats = db.obter_estatisticas(ativo_info['ativo'], dias=7)

                    if ultimo and stats:
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("💰 Preço Atual", f"${ultimo['preco']:,.2f}")

                        with col2:
                            st.metric("📉 Mínimo (7d)", f"${stats['preco_minimo']:,.2f}")

                        with col3:
                            st.metric("📈 Máximo (7d)", f"${stats['preco_maximo']:,.2f}")

                        with col4:
                            variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100
                            st.metric("📊 Variação", f"{variacao:.2f}%")

                except Exception as e:
                    st.error(f"Erro ao carregar dados: {e}")
    else:
        st.info("👉 Nenhum dado coletado ainda. Vá para **Coleta de Dados** para começar!")

    st.markdown("---")

    # Funcionalidades disponíveis
    st.subheader("🚀 Funcionalidades Disponíveis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📊 Dashboard
        - Visualização em tempo real
        - Gráficos interativos
        - Comparação entre ativos
        - Estatísticas detalhadas

        ### ⚡ Coleta de Dados
        - Coleta manual ou automática
        - Agendamento personalizado
        - Múltiplos coletores
        - Logs de execução
        """)

    with col2:
        st.markdown("""
        ### 🔍 Consultas
        - Histórico completo
        - Análises estatísticas
        - Exportação de dados
        - Comparação temporal

        ### 🔔 Alertas
        - Notificações Discord
        - Limites personalizados
        - Variações percentuais
        - Histórico de alertas
        """)

    st.markdown("---")

    # Status do sistema
    st.subheader("⚙️ Status do Sistema")

    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            db = DatabaseManager()
            st.success("✅ Banco de Dados: Conectado")
        except:
            st.error("❌ Banco de Dados: Erro")

    with col2:
        try:
            from dotenv import load_dotenv
            import os
            load_dotenv()
            webhook = os.getenv('DISCORD_WEBHOOK_URL')
            if webhook:
                st.success("✅ Discord: Configurado")
            else:
                st.warning("⚠️ Discord: Não configurado")
        except:
            st.error("❌ Discord: Erro")

    with col3:
        import os
        if os.path.exists('pipeline.pid'):
            st.success("✅ Serviço: Rodando")
        else:
            st.info("ℹ️ Serviço: Parado")

    st.markdown("---")

    # Início rápido
    st.subheader("🎯 Início Rápido")

    st.markdown("""
    1. **Configure o Discord** (opcional) em ⚙️ Configurações
    2. **Execute uma coleta** em ⚡ Coleta de Dados
    3. **Visualize os dados** em 📊 Dashboard
    4. **Configure alertas** em 🔔 Alertas
    """)

    # Footer
    st.markdown("---")
    st.caption(f"Sistema de Coleta Financeira v1.0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
