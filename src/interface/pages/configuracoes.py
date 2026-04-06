"""
Página de Configurações
"""

import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv, set_key

# Adicionar path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

load_dotenv()


def show():
    """Renderiza a página de configurações"""

    st.header("⚙️ Configurações do Sistema")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔔 Discord", "💾 Banco de Dados", "📊 Sistema"])

    with tab1:
        st.subheader("🔔 Configuração do Discord")

        st.info("""
        **Webhook do Discord**

        Para receber alertas no Discord, você precisa criar um webhook:

        1. Abra o Discord e acesse as configurações do seu servidor
        2. Vá em **Integrações** > **Webhooks**
        3. Clique em **Novo Webhook**
        4. Configure o nome e canal
        5. Copie a URL do webhook e cole abaixo
        """)

        # Status atual
        webhook_atual = os.getenv('DISCORD_WEBHOOK_URL', '')

        if webhook_atual:
            st.success("✅ Webhook configurado")
            # Mostrar apenas parte da URL por segurança
            webhook_display = webhook_atual[:50] + "..." if len(webhook_atual) > 50 else webhook_atual
            st.code(webhook_display, language='text')
        else:
            st.warning("⚠️ Webhook não configurado")

        st.markdown("---")

        # Formulário de configuração
        with st.form("discord_config"):
            nova_url = st.text_input(
                "URL do Webhook:",
                value=webhook_atual,
                type="password",
                help="Cole aqui a URL completa do webhook do Discord"
            )

            col1, col2 = st.columns([1, 3])

            with col1:
                submit = st.form_submit_button("💾 Salvar", type="primary")

            with col2:
                testar = st.form_submit_button("🧪 Testar Webhook")

            if submit:
                if nova_url:
                    salvar_webhook(nova_url)
                else:
                    st.error("❌ URL do webhook não pode estar vazia!")

            if testar:
                if nova_url:
                    testar_webhook(nova_url)
                else:
                    st.error("❌ Configure uma URL primeiro!")

    with tab2:
        st.subheader("💾 Banco de Dados")

        from database.db_manager import DatabaseManager

        try:
            db = DatabaseManager()

            # Informações do banco
            st.info(f"""
            **Localização:** `data/precos_cripto.db`

            **Tipo:** SQLite
            """)

            # Estatísticas
            ativos = db.listar_ativos()

            if ativos:
                st.markdown("#### 📊 Estatísticas")

                total_registros = sum(a['total_registros'] for a in ativos)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Ativos", len(ativos))

                with col2:
                    st.metric("Total de Registros", f"{total_registros:,}")

                with col3:
                    # Tamanho do arquivo
                    db_path = Path("data/precos_cripto.db")
                    if db_path.exists():
                        tamanho_mb = db_path.stat().st_size / (1024 * 1024)
                        st.metric("Tamanho", f"{tamanho_mb:.2f} MB")

                # Detalhes por ativo
                st.markdown("#### 📈 Detalhes por Ativo")

                for ativo in ativos:
                    with st.expander(f"{ativo['ativo']} - {ativo['total_registros']:,} registros"):
                        stats = db.obter_estatisticas(ativo['ativo'], dias=30)

                        if stats:
                            col1, col2 = st.columns(2)

                            with col1:
                                st.info(f"""
                                **Primeira coleta:** {stats['primeira_coleta']}

                                **Última coleta:** {stats['ultima_coleta']}
                                """)

                            with col2:
                                st.info(f"""
                                **Preço médio:** ${stats['preco_medio']:,.2f}

                                **Total registros:** {stats['total_registros']:,}
                                """)

            else:
                st.warning("Nenhum dado no banco. Execute uma coleta primeiro!")

            st.markdown("---")

            # Ações do banco
            st.markdown("#### ⚙️ Manutenção do Banco")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("🔄 Verificar Integridade", use_container_width=True):
                    verificar_integridade_banco()

            with col2:
                if st.button("📊 Otimizar Banco", use_container_width=True):
                    otimizar_banco()

            st.markdown("---")

            # Backup/Restauração
            st.markdown("#### 💾 Backup e Restauração")

            st.warning("⚠️ **Atenção:** Operações de backup devem ser feitas manualmente via terminal.")

            st.code("""
# Fazer backup
cp data/precos_cripto.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar backup
cp data/backup_YYYYMMDD_HHMMSS.db data/precos_cripto.db
            """, language='bash')

        except Exception as e:
            st.error(f"❌ Erro ao conectar ao banco de dados: {e}")

    with tab3:
        st.subheader("📊 Informações do Sistema")

        # Informações gerais
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📦 Versão")
            st.info("""
            **Sistema:** v1.0

            **Python:** 3.12+

            **Interface:** Streamlit
            """)

        with col2:
            st.markdown("#### 📁 Estrutura")
            st.info("""
            **Dados:** `data/`

            **Logs:** `logs/`

            **Código:** `src/`
            """)

        st.markdown("---")

        # Logs
        st.markdown("#### 📝 Logs do Sistema")

        log_files = {
            "Pipeline": "logs/pipeline.log",
            "Scheduler": "logs/scheduler.log",
            "Alertas": "logs/alertas.log",
            "Serviço": "logs/service.log"
        }

        log_selecionado = st.selectbox(
            "Selecione o log:",
            list(log_files.keys())
        )

        linhas = st.slider("Linhas a exibir:", 10, 100, 50)

        if st.button("📖 Carregar Log"):
            carregar_log(log_files[log_selecionado], linhas)

        st.markdown("---")

        # Ações do sistema
        st.markdown("#### ⚙️ Manutenção")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🧹 Limpar Logs", use_container_width=True):
                limpar_logs()

        with col2:
            if st.button("📊 Status Geral", use_container_width=True):
                mostrar_status_geral()

        with col3:
            if st.button("ℹ️ Sobre", use_container_width=True):
                mostrar_sobre()


def salvar_webhook(url):
    """Salva a URL do webhook no arquivo .env"""
    try:
        env_path = Path(".env")

        if not env_path.exists():
            # Criar arquivo .env se não existir
            with open(env_path, 'w') as f:
                f.write(f"DISCORD_WEBHOOK_URL={url}\n")
            st.success("✅ Webhook configurado com sucesso!")
        else:
            # Atualizar arquivo existente
            set_key(env_path, "DISCORD_WEBHOOK_URL", url)
            st.success("✅ Webhook atualizado com sucesso!")

        # Recarregar variáveis de ambiente
        load_dotenv(override=True)

    except Exception as e:
        st.error(f"❌ Erro ao salvar webhook: {e}")


def testar_webhook(url):
    """Testa a conexão com o webhook do Discord"""
    try:
        from utils.discord_notifier import DiscordNotifier

        notifier = DiscordNotifier(webhook_url=url)

        if notifier.testar_conexao():
            st.success("✅ Webhook testado com sucesso! Verifique seu Discord.")
        else:
            st.error("❌ Falha ao testar webhook. Verifique a URL.")

    except Exception as e:
        st.error(f"❌ Erro ao testar webhook: {e}")


def verificar_integridade_banco():
    """Verifica integridade do banco de dados"""
    try:
        import sqlite3

        conn = sqlite3.connect('data/precos_cripto.db')
        cursor = conn.cursor()

        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()

        conn.close()

        if result[0] == 'ok':
            st.success("✅ Banco de dados íntegro!")
        else:
            st.warning(f"⚠️ Problemas detectados: {result[0]}")

    except Exception as e:
        st.error(f"❌ Erro ao verificar integridade: {e}")


def otimizar_banco():
    """Otimiza o banco de dados"""
    try:
        import sqlite3

        conn = sqlite3.connect('data/precos_cripto.db')
        cursor = conn.cursor()

        cursor.execute("VACUUM")
        cursor.execute("ANALYZE")

        conn.close()

        st.success("✅ Banco de dados otimizado!")

    except Exception as e:
        st.error(f"❌ Erro ao otimizar banco: {e}")


def carregar_log(arquivo, linhas):
    """Carrega e exibe o log"""
    try:
        if Path(arquivo).exists():
            with open(arquivo, 'r') as f:
                todas_linhas = f.readlines()
                ultimas_linhas = ''.join(todas_linhas[-linhas:])

            st.code(ultimas_linhas, language='text')

        else:
            st.warning(f"⚠️ Arquivo de log não encontrado: {arquivo}")

    except Exception as e:
        st.error(f"❌ Erro ao carregar log: {e}")


def limpar_logs():
    """Limpa arquivos de log"""
    try:
        logs_dir = Path("logs")

        if logs_dir.exists():
            arquivos_removidos = 0

            for log_file in logs_dir.glob("*.log"):
                log_file.unlink()
                arquivos_removidos += 1

            st.success(f"✅ {arquivos_removidos} arquivo(s) de log removido(s)!")
        else:
            st.warning("⚠️ Diretório de logs não encontrado.")

    except Exception as e:
        st.error(f"❌ Erro ao limpar logs: {e}")


def mostrar_status_geral():
    """Mostra status geral do sistema"""
    st.markdown("### 📊 Status Geral do Sistema")

    # Banco de dados
    try:
        from database.db_manager import DatabaseManager
        db = DatabaseManager()
        st.success("✅ Banco de Dados: Conectado")
    except:
        st.error("❌ Banco de Dados: Erro")

    # Discord
    webhook = os.getenv('DISCORD_WEBHOOK_URL')
    if webhook:
        st.success("✅ Discord: Configurado")
    else:
        st.warning("⚠️ Discord: Não configurado")

    # Serviço em background
    if Path('pipeline.pid').exists():
        st.success("✅ Serviço em Background: Rodando")
    else:
        st.info("ℹ️ Serviço em Background: Parado")

    # Diretórios
    for diretorio in ['data', 'logs', 'src']:
        if Path(diretorio).exists():
            st.success(f"✅ Diretório '{diretorio}': OK")
        else:
            st.error(f"❌ Diretório '{diretorio}': Não encontrado")


def mostrar_sobre():
    """Mostra informações sobre o sistema"""
    st.markdown("""
    ### 📊 Sistema de Coleta Financeira

    **Versão:** 1.0

    **Descrição:**
    Sistema automatizado para coleta, análise e monitoramento de dados
    financeiros de criptomoedas.

    **Funcionalidades:**
    - ⚡ Coleta automática e agendada
    - 📊 Dashboard interativo com gráficos
    - 🔍 Consultas e análises estatísticas
    - 🔔 Sistema de alertas com Discord
    - 💾 Exportação de dados (CSV, JSON, Excel)
    - ⚙️ Interface gráfica moderna

    **Tecnologias:**
    - Python 3.12+
    - Streamlit (Interface)
    - SQLite (Banco de Dados)
    - Plotly (Gráficos)
    - Discord Webhooks (Notificações)


    """)
