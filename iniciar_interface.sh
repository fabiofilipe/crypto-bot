#!/bin/bash

# Script para inicializar a Interface Web
# Uso: ./iniciar_interface.sh

echo "========================================"
echo "🚀 Iniciando Interface Web"
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
echo "🌐 Interface: http://localhost:8501"
echo ""
$COMPOSE_CMD up -d web
echo ""
echo "🌐 Interface Web iniciada em background."
echo "Acessar:    http://localhost:8501"
echo "Ver logs:   $COMPOSE_CMD logs -f web"
echo "Parar:      $COMPOSE_CMD stop web"
