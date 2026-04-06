#  Sistema de Coleta Financeira

Sistema automatizado para coleta, análise e monitoramento de criptomoedas com interface web, bot Discord e alertas em tempo real.

##  Features

- **Bot Discord interativo** — `!crypto BTC`, `!comparar`, `!top`, `!todos`
- **Interface web moderna** — Streamlit com gráficos interativos
- **Coleta agendada** — 12+ criptos (BTC, ETH, SOL, DOGE, XRP, ADA, etc.)
- **PostgreSQL** — Banco robusto com histórico completo
- **Alertas Discord** — Notificações automáticas por webhook
- **Conversão BRL** — Preço em USD e Real brasileiro
- **Docker** — Deploy com um comando

---

## Quick Start

### Docker

```bash
cp .env.example .env   # edite DISCORD_BOT_TOKEN e DATABASE_URL
./scripts/docker.sh up
```

### Local

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m src.pipeline
```

---

##  Bot Discord

| Comando | Exemplo | Descrição |
|---|---|---|
| `!crypto BTC` | `!crypto SOL` | Relatório completo (preço, 24h, 7d, BRL) |
| `!comparar BTC ETH` | `!comparar BTC ETH` | Comparação lado a lado |
| `!top 5` | `!top 10` | Ranking por variação 24h |
| `!todos` | `!todos` | Status de todos os ativos |
| `!btc` / `!eth` | `!btc` | Atalhos rápidos |
| `!ativos` | `!ativos` | Lista ativos monitorados |
| `!ajuda` | `!ajuda` | Lista comandos |
| `alerta` | (no chat) | Trigger status de todos |

---

##  Interface Web

```bash
docker compose up -d web        # via Docker
streamlit run src/interface/app.py  # local
```

| Página | Descrição |
|---|---|
| **Home** | Visão geral e métricas |
| **Dashboard** | Gráficos (linha, candlestick, histograma) |
| **Coleta** | Executar e agendar coletas |
| **Consultas** | Histórico e exportação |
| **Alertas** | Configuração de limites |
| **Configurações** | Manutenção e logs |

---

##  Scripts

```bash
./scripts/docker.sh up          # Iniciar todos os serviços
./scripts/docker.sh down        # Parar
./scripts/docker.sh logs        # Ver logs
./scripts/docker.sh logs web    # Logs da interface
./scripts/docker.sh status      # Status dos containers
./scripts/iniciar_bot.sh        # Iniciar bot Discord
./scripts/iniciar_interface.sh  # Iniciar interface web
```

---

##  Estrutura

```
crypto-bot/
├── src/
│   ├── coletores/          # Coletores (BTC, ETH, genérico)
│   ├── database/           # PostgreSQL manager
│   ├── interface/          # Streamlit app + pages
│   ├── utils/              # Logger, Discord notifier, Coinbase API
│   ├── pipeline.py         # Orquestrador de coleta
│   ├── scheduler.py        # Agendador
│   ├── alertas.py          # Sistema de alertas
│   └── bot_discord.py      # Bot Discord
├── docs/                   # Documentação
├── scripts/                # Scripts de deploy
├── tests/                  # Testes
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

##  Tecnologias

- **Python 3.12** · **PostgreSQL 17** · **Docker**
- **Streamlit** · **Plotly** · **Discord.py**
- **Coinbase API** (pública, sem key)

---

##  Configuração

### .env

```env
DATABASE_URL=postgresql://crypto_user:crypto_pass@localhost:5432/crypto_bot
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/ID/TOKEN
DISCORD_BOT_TOKEN=seu_token_aqui
```

### Criar Bot Discord

1. Acesse https://discord.com/developers/applications
2. Crie Application → Bot → Copy Token
3. Ative **Message Content Intent**
4. Invite o bot com OAuth2 URL Generator (scopes: `bot`, perms: `Send Messages`, `Embed Links`)

---

##  Desenvolvimento

### Adicionar nova cripto

Basta adicionar ao `ATIVOS_DISPONIVEIS` em `src/pipeline.py`:

```python
ATIVOS_DISPONIVEIS = [
    ("BTC", "Bitcoin"),
    ("PEPE", "Pepe"),  # nova!
]
```

O coletor genérico (`ColetorDinamico`) cuida do resto.

### Rodar testes

```bash
pytest tests/
```

---

##  Licença

MIT — veja [LICENSE](LICENSE).

---

##  Roadmap

- [ ] Testes unitários
- [ ] CI/CD com GitHub Actions
- [ ] Mais exchanges (Binance, CoinGecko)
- [ ] Alertas configuráveis por usuário no Discord
- [ ] API REST
- [ ] Modo paper trading
