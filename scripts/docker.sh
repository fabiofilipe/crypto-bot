#!/bin/bash

# Script de utilidade para Docker
# Uso: ./docker.sh [build|up|down|logs|restart|status|clean]

COMPOSE_CMD="docker compose"
if ! docker compose version &> /dev/null && command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
fi

case "$1" in
    build)
        echo "🔨 Construindo imagens..."
        $COMPOSE_CMD build --no-cache
        ;;
    up)
        echo "🚀 Iniciando todos os serviços..."
        mkdir -p data logs
        $COMPOSE_CMD up -d
        echo "✅ Serviços iniciados:"
        $COMPOSE_CMD ps
        ;;
    down)
        echo "🛑 Parando todos os serviços..."
        $COMPOSE_CMD down
        ;;
    logs)
        SERVICE="${2:-}"
        if [ -z "$SERVICE" ]; then
            $COMPOSE_CMD logs -f
        else
            $COMPOSE_CMD logs -f "$SERVICE"
        fi
        ;;
    restart)
        echo "🔄 Reiniciando serviços..."
        $COMPOSE_CMD restart
        ;;
    status)
        $COMPOSE_CMD ps
        ;;
    clean)
        echo "🧹 Limpando containers e imagens..."
        $COMPOSE_CMD down --rmi local --volumes
        ;;
    *)
        echo "Uso: $0 {build|up|down|logs [service]|restart|status|clean}"
        echo ""
        echo "Comandos:"
        echo "  build    - Construir imagens Docker"
        echo "  up       - Iniciar todos os serviços"
        echo "  down     - Parar todos os serviços"
        echo "  logs     - Ver logs (opcional: logs <servico>)"
        echo "  restart  - Reiniciar serviços"
        echo "  status   - Ver status dos serviços"
        echo "  clean    - Remover containers e imagens"
        exit 1
        ;;
esac
