#!/bin/bash

# Script para inicializar a interface web
# Uso: ./iniciar_interface.sh

echo "========================================"
echo "🚀 Iniciando Interface Web"
echo "========================================"

# Verificar se está no diretório correto
if [ ! -d "src/interface" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto"
    exit 1
fi

# Ativar ambiente virtual
if [ -d ".venv" ]; then
    echo "✅ Ativando ambiente virtual..."
    source .venv/bin/activate
else
    echo "❌ Ambiente virtual não encontrado em .venv"
    exit 1
fi

# Verificar se streamlit está instalado
if ! python -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Streamlit não encontrado. Instalando dependências..."
    pip install -r requirements_web.txt
fi

# Criar diretórios necessários
mkdir -p data logs

# Iniciar aplicação
echo ""
echo "========================================"
echo "🌐 Abrindo interface web..."
echo "========================================"
echo ""
echo "A interface será aberta automaticamente no navegador."
echo "URL: http://localhost:8501"
echo ""
echo "Pressione Ctrl+C para encerrar"
echo ""

# Executar streamlit
streamlit run src/interface/app.py
