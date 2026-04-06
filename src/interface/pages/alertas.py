"""
Página de Alertas
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from alertas import SistemaAlertas
from database.db_manager import DatabaseManager


def show():
    """Renderiza a página de alertas"""

    st.header("🔔 Sistema de Alertas")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["⚡ Verificar Alertas", "⚙️ Configurar Limites", "📤 Enviar Status", "📋 Histórico"])

    with tab1:
        st.subheader("⚡ Verificação de Alertas")

        st.info("""
        **Como funciona:**
        - Compara o preço atual com o preço anterior
        - Detecta variações acima do limite configurado
        - Envia notificações no terminal e Discord (se configurado)
        """)

        col1, col2 = st.columns([2, 1])

        with col1:
            limite_percentual = st.slider(
                "Limite de variação (%):",
                min_value=1.0,
                max_value=20.0,
                value=3.0,
                step=0.5,
                help="Será notificado se a variação exceder este valor"
            )

        with col2:
            discord_enabled = st.checkbox("Enviar para Discord", value=True)

        st.markdown("---")

        # Botões de ação
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔔 Verificar Todos os Ativos", type="primary", use_container_width=True):
                verificar_todos_alertas(limite_percentual, discord_enabled)

        with col2:
            db = DatabaseManager()
            ativos = db.listar_ativos()

            if ativos:
                ativo_individual = st.selectbox(
                    "Ou verificar apenas:",
                    [a['ativo'] for a in ativos]
                )

                if st.button("🔍 Verificar Ativo Individual", use_container_width=True):
                    verificar_alerta_individual(ativo_individual, limite_percentual, discord_enabled)

    with tab2:
        st.subheader("⚙️ Configurar Limites de Preço")

        st.warning("""
        ⚠️ **Atenção:** Limites de preço enviam alertas quando o preço ultrapassa valores mínimos ou máximos definidos.
        Esta configuração é temporária e não persiste entre sessões.
        """)

        db = DatabaseManager()
        ativos = db.listar_ativos()

        if ativos:
            ativo_config = st.selectbox(
                "Selecione o ativo:",
                [a['ativo'] for a in ativos],
                key="config_ativo"
            )

            # Mostrar preço atual
            ultimo = db.obter_ultimo_preco(ativo_config)
            if ultimo:
                st.metric("💰 Preço Atual", f"${ultimo['preco']:,.2f}")

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                habilitar_minimo = st.checkbox("Habilitar alerta de mínimo")
                if habilitar_minimo:
                    preco_minimo = st.number_input(
                        "Preço mínimo ($):",
                        min_value=0.0,
                        value=float(ultimo['preco'] * 0.9) if ultimo else 0.0,
                        step=100.0,
                        format="%.2f"
                    )
                else:
                    preco_minimo = None

            with col2:
                habilitar_maximo = st.checkbox("Habilitar alerta de máximo")
                if habilitar_maximo:
                    preco_maximo = st.number_input(
                        "Preço máximo ($):",
                        min_value=0.0,
                        value=float(ultimo['preco'] * 1.1) if ultimo else 0.0,
                        step=100.0,
                        format="%.2f"
                    )
                else:
                    preco_maximo = None

            st.markdown("---")

            if st.button("🔔 Verificar Limites", type="primary"):
                verificar_limites_preco(ativo_config, preco_minimo, preco_maximo)

        else:
            st.warning("Nenhum ativo disponível. Execute uma coleta primeiro!")

    with tab3:
        st.subheader("📤 Enviar Status Atual para Discord")

        st.info("""
        **Envie o preço atual de qualquer ativo para o Discord a qualquer momento!**

        Não precisa esperar por variações - envie quando quiser verificar o status.
        """)

        db = DatabaseManager()
        ativos = db.listar_ativos()

        if ativos:
            col1, col2 = st.columns([2, 1])

            with col1:
                ativo_enviar = st.selectbox(
                    "Selecione o ativo:",
                    [a['ativo'] for a in ativos],
                    key="enviar_status_ativo"
                )

            with col2:
                incluir_stats = st.checkbox("Incluir estatísticas", value=True)

            # Mostrar preview do que será enviado
            st.markdown("---")
            st.markdown("### 👁️ Preview")

            try:
                ultimo = db.obter_ultimo_preco(ativo_enviar)

                if ultimo:
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("💰 Preço Atual", f"${ultimo['preco']:,.2f}")

                    with col2:
                        st.metric("💱 Moeda", ultimo['moeda'])

                    with col3:
                        st.metric("🕐 Última Coleta", ultimo['horario_coleta'].split()[1][:5])

                    if incluir_stats:
                        stats = db.obter_estatisticas(ativo_enviar, dias=7)
                        if stats:
                            st.markdown("**Estatísticas (7 dias):**")
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.info(f"Mín: ${stats['preco_minimo']:,.2f}")

                            with col2:
                                st.info(f"Média: ${stats['preco_medio']:,.2f}")

                            with col3:
                                st.info(f"Máx: ${stats['preco_maximo']:,.2f}")

            except Exception as e:
                st.error(f"Erro ao carregar preview: {e}")

            st.markdown("---")

            # Botão de envio
            col1, col2, col3 = st.columns([1, 1, 1])

            with col2:
                if st.button("📤 Enviar para Discord", type="primary", use_container_width=True):
                    enviar_status_discord(ativo_enviar, incluir_stats)

            # Atalho rápido - enviar todos os ativos
            st.markdown("---")
            st.markdown("### 🚀 Atalho Rápido")

            if st.button("📤 Enviar Status de TODOS os Ativos", use_container_width=True):
                enviar_todos_ativos_discord()

        else:
            st.warning("Nenhum ativo disponível. Execute uma coleta primeiro!")

    with tab4:
        st.subheader("📋 Histórico de Alertas")

        st.info("""
        Mostra os alertas mais recentes detectados na sessão atual.
        O histórico é resetado quando o sistema é reiniciado.
        """)

        try:
            sistema = SistemaAlertas(discord_habilitado=False)
            historico = sistema.obter_historico_alertas(limite=20)

            if historico:
                for alerta in historico:
                    tipo = alerta.get('tipo', 'DESCONHECIDO')

                    if tipo == 'ALTA':
                        emoji = "📈"
                        cor = "green"
                    elif tipo == 'BAIXA':
                        emoji = "📉"
                        cor = "red"
                    elif tipo == 'ABAIXO_MINIMO':
                        emoji = "⚠️"
                        cor = "red"
                    elif tipo == 'ACIMA_MAXIMO':
                        emoji = "⚠️"
                        cor = "orange"
                    else:
                        emoji = "🔔"
                        cor = "blue"

                    with st.expander(f"{emoji} {alerta.get('ativo', 'N/A')} - {alerta.get('timestamp', 'N/A')}"):
                        if 'variacao' in alerta:
                            st.metric(
                                "Variação",
                                f"{alerta['variacao']:+.2f}%",
                                delta=f"{alerta['variacao']:+.2f}%"
                            )

                            col1, col2 = st.columns(2)

                            with col1:
                                st.info(f"**Preço Anterior:** ${alerta.get('preco_anterior', 0):,.2f}")

                            with col2:
                                st.info(f"**Preço Atual:** ${alerta.get('preco_atual', 0):,.2f}")
                        else:
                            col1, col2 = st.columns(2)

                            with col1:
                                st.info(f"**Preço Atual:** ${alerta.get('preco_atual', 0):,.2f}")

                            with col2:
                                st.info(f"**Limite:** ${alerta.get('limite', 0):,.2f}")

            else:
                st.info("Nenhum alerta registrado na sessão atual.")

        except Exception as e:
            st.error(f"Erro ao carregar histórico: {e}")


def verificar_todos_alertas(limite_percentual, discord_enabled):
    """Verifica alertas para todos os ativos"""

    with st.status("Verificando alertas...", expanded=True) as status:
        try:
            st.write("🔍 Analisando variações de preço...")

            sistema = SistemaAlertas(discord_habilitado=discord_enabled)
            alertas = sistema.verificar_todos_ativos(limite_percentual=limite_percentual)

            status.update(label="Verificação concluída!", state="complete")

            if alertas:
                st.warning(f"⚠️ {len(alertas)} alerta(s) detectado(s)!")

                for alerta in alertas:
                    emoji = "📈" if alerta['tipo'] == 'ALTA' else "📉"
                    cor = "green" if alerta['tipo'] == 'ALTA' else "red"

                    with st.container():
                        st.markdown(f"### {emoji} {alerta['ativo']}")

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.metric(
                                "Variação",
                                f"{alerta['variacao']:+.2f}%",
                                delta=f"{alerta['variacao']:+.2f}%"
                            )

                        with col2:
                            st.metric(
                                "Preço Anterior",
                                f"${alerta['preco_anterior']:,.2f}"
                            )

                        with col3:
                            st.metric(
                                "Preço Atual",
                                f"${alerta['preco_atual']:,.2f}"
                            )

                        st.markdown("---")

            else:
                st.success("✅ Nenhuma variação significativa detectada!")

        except Exception as e:
            status.update(label="Erro na verificação", state="error")
            st.error(f"❌ Erro: {e}")


def verificar_alerta_individual(ativo, limite_percentual, discord_enabled):
    """Verifica alerta para um ativo específico"""

    with st.status(f"Verificando {ativo}...", expanded=True) as status:
        try:
            st.write(f"🔍 Analisando variação de {ativo}...")

            sistema = SistemaAlertas(discord_habilitado=discord_enabled)
            alerta = sistema.verificar_variacao_percentual(ativo, limite_percentual)

            status.update(label="Verificação concluída!", state="complete")

            if alerta:
                emoji = "📈" if alerta['tipo'] == 'ALTA' else "📉"

                st.warning(f"{emoji} Alerta detectado para {ativo}!")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Variação",
                        f"{alerta['variacao']:+.2f}%",
                        delta=f"{alerta['variacao']:+.2f}%"
                    )

                with col2:
                    st.metric(
                        "Preço Anterior",
                        f"${alerta['preco_anterior']:,.2f}"
                    )

                with col3:
                    st.metric(
                        "Preço Atual",
                        f"${alerta['preco_atual']:,.2f}"
                    )

            else:
                st.success(f"✅ Nenhuma variação significativa para {ativo}")

        except Exception as e:
            status.update(label="Erro na verificação", state="error")
            st.error(f"❌ Erro: {e}")


def verificar_limites_preco(ativo, preco_minimo, preco_maximo):
    """Verifica se o preço ultrapassou limites"""

    with st.status("Verificando limites...", expanded=True) as status:
        try:
            st.write(f"🔍 Verificando limites de {ativo}...")

            sistema = SistemaAlertas()
            alertas = sistema.verificar_limite_preco(ativo, preco_minimo, preco_maximo)

            status.update(label="Verificação concluída!", state="complete")

            if alertas:
                st.warning(f"⚠️ {len(alertas)} alerta(s) de limite detectado(s)!")

                for alerta in alertas:
                    tipo_msg = "ABAIXO DO MÍNIMO" if alerta['tipo'] == 'ABAIXO_MINIMO' else "ACIMA DO MÁXIMO"

                    st.error(f"⚠️ **{tipo_msg}**")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Preço Atual", f"${alerta['preco_atual']:,.2f}")

                    with col2:
                        st.metric("Limite Definido", f"${alerta['limite']:,.2f}")

            else:
                st.success("✅ Preço dentro dos limites definidos!")

        except Exception as e:
            status.update(label="Erro na verificação", state="error")
            st.error(f"❌ Erro: {e}")


def enviar_status_discord(ativo, incluir_stats=True):
    """Envia o status atual de um ativo para o Discord"""

    with st.status(f"Enviando status de {ativo}...", expanded=True) as status:
        try:
            from utils.discord_notifier import DiscordNotifier

            st.write("📡 Conectando ao Discord...")

            notifier = DiscordNotifier()
            db = DatabaseManager()

            # Buscar dados
            ultimo = db.obter_ultimo_preco(ativo)

            if not ultimo:
                st.error("❌ Nenhum dado disponível para este ativo!")
                status.update(label="Erro ao buscar dados", state="error")
                return

            st.write("📊 Preparando mensagem...")

            # Criar mensagem
            if incluir_stats:
                stats = db.obter_estatisticas(ativo, dias=7)

                if stats:
                    variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

                    mensagem = f"""
**📊 Status Atual - {ativo}**

💰 **Preço Atual:** ${ultimo['preco']:,.2f} {ultimo['moeda']}
🕐 **Última Coleta:** {ultimo['horario_coleta']}

**Estatísticas (7 dias):**
📉 Mínimo: ${stats['preco_minimo']:,.2f}
📊 Médio: ${stats['preco_medio']:,.2f}
📈 Máximo: ${stats['preco_maximo']:,.2f}
📊 Variação: {variacao:.2f}%
📋 Registros: {stats['total_registros']}

_Enviado via Interface Web_
"""
                else:
                    mensagem = f"""
**📊 Status Atual - {ativo}**

💰 **Preço Atual:** ${ultimo['preco']:,.2f} {ultimo['moeda']}
🕐 **Última Coleta:** {ultimo['horario_coleta']}

_Enviado via Interface Web_
"""
            else:
                mensagem = f"""
**📊 Status Atual - {ativo}**

💰 **Preço Atual:** ${ultimo['preco']:,.2f} {ultimo['moeda']}
🕐 **Última Coleta:** {ultimo['horario_coleta']}

_Enviado via Interface Web_
"""

            st.write("🚀 Enviando para Discord...")

            # Enviar
            if notifier.enviar_mensagem_simples(mensagem):
                status.update(label="Enviado com sucesso!", state="complete")
                st.success(f"✅ Status de {ativo} enviado para o Discord!")

                # Mostrar preview
                with st.expander("👁️ Mensagem enviada"):
                    st.code(mensagem, language='text')
            else:
                status.update(label="Erro ao enviar", state="error")
                st.error("❌ Falha ao enviar para Discord!")

        except Exception as e:
            status.update(label="Erro", state="error")
            st.error(f"❌ Erro ao enviar: {e}")


def enviar_todos_ativos_discord():
    """Envia status de todos os ativos para o Discord"""

    with st.status("Enviando status de todos os ativos...", expanded=True) as status:
        try:
            from utils.discord_notifier import DiscordNotifier

            st.write("📡 Conectando ao Discord...")

            notifier = DiscordNotifier()
            db = DatabaseManager()

            # Buscar todos os ativos
            ativos = db.listar_ativos()

            if not ativos:
                st.error("❌ Nenhum ativo disponível!")
                status.update(label="Erro", state="error")
                return

            st.write(f"📊 Coletando dados de {len(ativos)} ativo(s)...")

            # Criar mensagem consolidada
            mensagem = "**📊 Status de Todos os Ativos**\n\n"

            for ativo_info in ativos:
                ativo = ativo_info['ativo']
                ultimo = db.obter_ultimo_preco(ativo)
                stats = db.obter_estatisticas(ativo, dias=7)

                if ultimo and stats:
                    variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100

                    mensagem += f"""
**{ativo}**
💰 Preço: ${ultimo['preco']:,.2f} {ultimo['moeda']}
📊 Variação 7d: {variacao:+.2f}%
📈 Máx: ${stats['preco_maximo']:,.2f} | 📉 Mín: ${stats['preco_minimo']:,.2f}

"""

            mensagem += f"\n🕐 Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n_Enviado via Interface Web_"

            st.write("🚀 Enviando para Discord...")

            # Enviar
            if notifier.enviar_mensagem_simples(mensagem):
                status.update(label="Enviado com sucesso!", state="complete")
                st.success(f"✅ Status de {len(ativos)} ativo(s) enviado para o Discord!")

                # Mostrar preview
                with st.expander("👁️ Mensagem enviada"):
                    st.code(mensagem, language='text')
            else:
                status.update(label="Erro ao enviar", state="error")
                st.error("❌ Falha ao enviar para Discord!")

        except Exception as e:
            status.update(label="Erro", state="error")
            st.error(f"❌ Erro ao enviar: {e}")
