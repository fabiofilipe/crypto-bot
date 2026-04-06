#!/bin/bash

# Script para inicializar o Bot Discord
# Uso: ./iniciar_bot.sh

echo "========================================"
echo "🤖 Iniciando Bot Discord"
echo "========================================"

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Erro: Execute este script da raiz do projeto"
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instale: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não encontrado."
    exit 1
fi

mkdir -p data logs

COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null && command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
fi

echo ""
echo "✅ Iniciando container..."
echo ""
$COMPOSE_CMD up -d discord-bot
echo ""
echo "🤖 Bot Discord iniciado em background."
echo "Ver logs: $COMPOSE_CMD logs -f discord-bot"
echo "Parar:    $COMPOSE_CMD stop discord-bot"
