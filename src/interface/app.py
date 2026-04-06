"""
Interface Gráfica Principal - Sistema de Coleta Financeira
Execute: streamlit run src/interface/app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configuração da página
st.set_page_config(
    page_title="Sistema de Coleta Financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS customizado
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
        padding-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.title("💰 Sistema de Coleta Financeira")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/bitcoin.png", width=80)
    st.title("Navegação")
    st.markdown("---")

    # Menu de navegação
    page = st.radio(
        "Escolha uma funcionalidade:",
        [
            "🏠 Home",
            "📊 Dashboard",
            "⚡ Coleta de Dados",
            "🔍 Consultas",
            "🔔 Alertas",
            "⚙️ Configurações"
        ]
    )

    st.markdown("---")
    st.markdown("### Sobre")
    st.info(
        "Sistema automatizado para coleta e análise "
        "de dados financeiros de criptomoedas."
    )

# Conteúdo principal baseado na página selecionada
if page == "🏠 Home":
    from pages import home
    home.show()
elif page == "📊 Dashboard":
    from pages import dashboard
    dashboard.show()
elif page == "⚡ Coleta de Dados":
    from pages import coleta
    coleta.show()
elif page == "🔍 Consultas":
    from pages import consultas
    consultas.show()
elif page == "🔔 Alertas":
    from pages import alertas
    alertas.show()
elif page == "⚙️ Configurações":
    from pages import configuracoes
    configuracoes.show()
