# Skill: Setup Rápido de Ambiente

## Descrição
Configura o ambiente de desenvolvimento do zero para um novo desenvolvedor ou máquina.

## Como Usar
Quando o usuário pedir "configure meu ambiente" ou "setup do projeto".

## Processo

### 1. Pré-requisitos
```bash
# Verificar dependências
python3 --version        # Deve ser 3.12+
docker --version          # Docker instalado
docker compose version    # Docker Compose instalado
```

### 2. Clone e Setup Inicial
```bash
cd /home/fabiof/Projeto-coleta-financeira
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configuração de Ambiente
```bash
cp .env.example .env
# Editar .env com:
# - DATABASE_URL
# - DISCORD_WEBHOOK_URL (opcional)
# - DISCORD_BOT_TOKEN (opcional)
```

### 4. Docker Services
```bash
./scripts/docker.sh up
# Aguardar postgres ficar healthy
./scripts/docker.sh status
```

### 5. Verificação
```bash
# Testar coleta única
PYTHONPATH=src python -m src.pipeline

# Verificar dados no banco
PYTHONPATH=src python -c "
from database.db_manager import DatabaseManager
db = DatabaseManager()
print(db.obter_resumo_mercado())
"

# Verificar interface
curl http://localhost:8501
```

### 6. Testes (quando existirem)
```bash
pip install pytest pytest-mock
pytest tests/ -v
```

## Troubleshooting

### PostgreSQL não inicia
```bash
docker compose logs postgres
# Se porta 5432 em uso:
lsof -i :5432
# Matar processo ou mudar porta no docker-compose
```

### ModuleNotFoundError
```bash
export PYTHONPATH=/home/fabiof/Projeto-coleta-financeira/src
# Ou adicionar ao .bashrc:
echo 'export PYTHONPATH=/home/fabiof/Projeto-coleta-financeira/src' >> ~/.bashrc
```

### Discord Bot não conecta
```bash
# Verificar token:
cat .env | grep DISCORD_BOT_TOKEN
# Verificar intents no Discord Developer Portal:
# - Message Content Intent: ON
# - Server Members Intent: ON (opcional)
```

## Output
Ambiente configurado e verificado. Todos os services rodando.
