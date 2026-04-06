#!/bin/bash

# Script para executar o pipeline como serviço em background
# Uso: ./run_service.sh start|stop|status|restart

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PID_FILE="$SCRIPT_DIR/pipeline.pid"
LOG_FILE="$SCRIPT_DIR/logs/service.log"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "❌ Serviço já está rodando (PID: $PID)"
            exit 1
        fi
    fi
    
    echo "🚀 Iniciando serviço de coleta..."
    cd "$SCRIPT_DIR"
    
    # Ativar ambiente virtual 
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    
    # Executar em background
    nohup python src/scheduler.py > "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo "✅ Serviço iniciado (PID: $PID)"
    echo "📝 Logs em: $LOG_FILE"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "❌ Serviço não está rodando"
        exit 1
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "🛑 Parando serviço (PID: $PID)..."
        kill $PID
        rm "$PID_FILE"
        echo "✅ Serviço parado"
    else
        echo "❌ Processo não encontrado (PID: $PID)"
        rm "$PID_FILE"
    fi
}

status() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⭕ Serviço não está rodando"
        exit 0
    fi
    
    PID=$(cat "$PID_FILE")
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Serviço está rodando (PID: $PID)"
        
        # Mostrar últimas linhas do log
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "📝 Últimas linhas do log:"
            tail -n 10 "$LOG_FILE"
        fi
    else
        echo "❌ Serviço parado (PID inválido: $PID)"
        rm "$PID_FILE"
    fi
}

restart() {
    echo "🔄 Reiniciando serviço..."
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        restart
        ;;
    *)
        echo "Uso: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac