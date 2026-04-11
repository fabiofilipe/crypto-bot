# Reference Card — Sistema de Coleta Financeira & Qwen

## Project at a Glance

```
Crypto price collector → PostgreSQL → Discord alerts + Web UI
12 cryptos | Coinbase API | Docker | Python 3.12
```

## Quick Commands

```bash
# Start/Stop
./scripts/docker.sh up          # Start all services
./scripts/docker.sh down        # Stop all
./scripts/docker.sh status      # Check status
./scripts/docker.sh logs        # View logs

# Development
python -m src.bot_discord       # Run bot locally
streamlit run src/interface/app.py  # Run web UI locally
python -m src.pipeline          # Run single collection
python -m src.scheduler         # Run scheduled collection

# Testing
pytest tests/                   # Run tests
```

## Key Files

| File | Purpose |
|------|---------|
| `src/pipeline.py` | Collection orchestrator (add cryptos here) |
| `src/bot_discord.py` | Discord bot commands |
| `src/alertas.py` | Price alert system |
| `src/scheduler.py` | Scheduled collection |
| `src/database/db_manager.py` | All database operations |
| `src/interface/app.py` | Streamlit web interface |
| `src/coletores/dinamico.py` | Generic crypto collector |
| `src/utils/coinbase_api.py` | Coinbase API wrapper |
| `src/utils/discord_notifier.py` | Discord webhook notifications |

## Architecture

```
Coinbase API → ColetorDinamico → PipelineColeta → PostgreSQL
                                          ↓
                                   SistemaAlertas → Discord Webhook
                                          ↓
                              Discord Bot (interactive commands)
                              Streamlit Web UI (6 pages)
```

## Qwen Tools Quick Reference

### Agents
```
# Fast exploration
agent(Explore): "Find all Discord commands" (quick)
agent(Explore): "Map database schema" (medium)
agent(Explore): "Understand full data flow" (very thorough)

# Complex tasks
agent(general-purpose): "Add Binance support"
agent(general-purpose): "Write unit tests"
agent(general-purpose): "Refactor alert system"
```

### Skills
```
/review src/bot_discord.py          # Review code
/loop 10m check build               # Recurring task
/qc-helper how to configure MCP     # Qwen help
/find-skills                        # Discover new skills
```

### MCP Servers (configure in Qwen settings)
```
postgres    → Query collected data
docker      → Manage containers
github      → PR reviews, issues
filesystem  → Navigate project
git         → History, blame, diff
playwright  → Browser automation, UI testing, web scraping
```

## Common Tasks with Qwen

| Task | Prompt |
|------|--------|
| Add crypto | "Add PEPE to ATIVOS_DISPONIVEIS in src/pipeline.py" |
| Write tests | "Write unit tests for src/alertas.py" |
| New feature | "Implement REST API for price queries" |
| Fix bug | "Fix the !comparar command in src/bot_discord.py" |
| Review code | "/review src/alertas.py" |
| Explore code | "Explore how alerts work" |
| Docker help | "Check why collector isn't starting" |

## Project Conventions

1. Read files before editing
2. Use `db_manager.py` for all database access
3. Follow existing code style (Portuguese comments where they exist)
4. Add tests when implementing features
5. Log through `src/utils/logger.py`
6. Error handling: retry pattern from `ColetorBase`

## Environment Variables

```env
DATABASE_URL=postgresql://crypto_user:crypto_pass@localhost:5432/crypto_bot
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/ID/TOKEN
DISCORD_BOT_TOKEN=your_token_here
```

## Roadmap (Not Yet Implemented)

- [ ] Unit tests
- [ ] CI/CD with GitHub Actions
- [ ] Multiple exchanges (Binance, CoinGecko)
- [ ] Per-user Discord alert thresholds
- [ ] REST API
- [ ] Paper trading mode
