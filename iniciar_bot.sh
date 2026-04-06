#!/bin/bash

# Script para inicializar o bot Discord
# Uso: ./iniciar_bot.sh

echo "========================================"
echo "🤖 Iniciando Bot Discord"
echo "========================================"

# Verificar se está no diretório correto
if [ ! -d "src" ]; then
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

# Verificar se discord.py está instalado
if ! python -c "import discord" 2>/dev/null; then
    echo "⚠️  discord.py não encontrado. Instalando dependências..."
    pip install discord.py
fi

# Verificar se o token está configurado
if ! grep -q "DISCORD_BOT_TOKEN=" .env 2>/dev/null; then
    echo "⚠️  DISCORD_BOT_TOKEN não encontrado no .env"
    echo ""
    echo "📝 Configure o token do bot:"
    echo "1. Acesse: https://discord.com/developers/applications"
    echo "2. Crie uma Application e adicione um Bot"
    echo "3. Copie o token"
    echo "4. Adicione no arquivo .env:"
    echo "   DISCORD_BOT_TOKEN=seu_token_aqui"
    echo ""
    read -p "Pressione Enter para continuar mesmo assim ou Ctrl+C para cancelar..."
fi

# Criar diretórios necessários
mkdir -p logs

# Iniciar bot
echo ""
echo "========================================"
echo "🤖 Iniciando bot..."
echo "========================================"
echo ""
echo "O bot ficará ativo e responderá a comandos no Discord."
echo ""
echo "Comandos disponíveis:"
echo "  - Digite 'alerta' em qualquer mensagem"
echo "  - !preco BTC"
echo "  - !status ETH"
echo "  - !btc ou !eth"
echo "  - !todos"
echo "  - !ajuda"
echo ""
echo "Pressione Ctrl+C para encerrar"
echo ""

# Executar bot
python src/bot_discord.py
