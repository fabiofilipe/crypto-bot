---
name: setup-rapido
description: Configura ambiente de desenvolvimento do zero. Use para "configure meu ambiente", "setup do projeto".
---

## Processo
1. **Venv + Deps**: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. **Env**: `cp .env.example .env` e edite DATABASE_URL, DISCORD_WEBHOOK_URL, DISCORD_BOT_TOKEN
3. **Docker**: `./scripts/docker.sh up` e aguarde postgres healthy
4. **Verificação**: `PYTHONPATH=src python -m src.pipeline` e `curl http://localhost:8501`

## Troubleshooting
- **PostgreSQL não inicia**: `docker compose logs postgres` — se porta 5432 em uso: `lsof -i :5432`
- **ModuleNotFoundError**: `export PYTHONPATH=$(pwd)/src`
- **Discord não conecta**: Verifique token e Message Content Intent no Developer Portal
