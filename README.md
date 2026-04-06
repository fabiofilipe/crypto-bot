#  Sistema de Coleta Financeira

Sistema automatizado completo para coleta, análise e monitoramento de dados financeiros de criptomoedas, com interface gráfica moderna e sistema de alertas via Discord.

##  Características

- **Interface Web Moderna** - Interface gráfica completa com Streamlit
- **Coleta Automática** - Agendamento flexível de coletas
- **Dashboard Interativo** - Gráficos e análises em tempo real
- **Alertas Inteligentes** - Notificações Discord para variações
- **Análises Avançadas** - Estatísticas e comparações detalhadas
- **Múltiplas Exportações** - CSV, JSON e Excel
- **Banco SQLite** - Armazenamento local eficiente
- **Logs Detalhados** - Rastreamento completo de operações

---

## Início Rápido

### 1. Instalação

```bash
# Clone o repositório
git clone <url-do-repo>
cd Projeto-coleta-financeira

# Crie e ative o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependências básicas
pip install -r requirements.txt

# Instale as dependências da interface web
pip install -r requirements_web.txt
```

### 2. Iniciar Interface Gráfica

```bash
./iniciar_interface.sh
```

A interface será aberta automaticamente em: **http://localhost:8501**

### 3. Primeira Coleta

Através da interface web:
1. Acesse **Coleta de Dados**
2. Clique em **Executar Pipeline Completo**
3. Aguarde a conclusão

Ou via terminal:
```bash
.venv/bin/python3 src/pipeline.py
```

---

##  Interface Gráfica

###  Home
- Visão geral do sistema
- Métricas principais
- Status de serviços
- Guia de início rápido

###  Dashboard
- Gráficos interativos (linha, candlestick, histograma)
- Estatísticas em tempo real
- Comparação entre ativos
- Análise de volatilidade

###  Coleta de Dados
- Execução manual de coletas
- Agendamento automático
- Histórico de coletas
- Logs em tempo real

###  Consultas
- Estatísticas detalhadas
- Histórico completo
- Comparação de ativos
- Exportação de dados

###  Alertas
- Verificação de variações
- Configuração de limites
- Histórico de alertas
- Integração com Discord

###  Configurações
- Configuração do Discord
- Gerenciamento do banco
- Visualização de logs
- Manutenção do sistema

---

## Modo Terminal

### Comandos Principais

```bash
# Coleta única
.venv/bin/python3 src/pipeline.py

# Coleta agendada
.venv/bin/python3 src/scheduler.py

# Consultas interativas
.venv/bin/python3 src/consulta.py

# Dashboard terminal
.venv/bin/python3 src/dashboard.py

# Verificar alertas
.venv/bin/python3 src/alertas.py

# Testar Discord
.venv/bin/python3 testar_discord.py
```

### Serviço em Background

```bash
# Iniciar
./run_service.sh start

# Parar
./run_service.sh stop

# Status
./run_service.sh status

# Reiniciar
./run_service.sh restart
```

---

##  Configurar Discord

### 1. Criar Webhook

1. Abra o Discord
2. Configurações do Servidor > Integrações > Webhooks
3. Clique em "Novo Webhook"
4. Configure nome e canal
5. Copie a URL do webhook

### 2. Configurar no Sistema

**Via Interface Web:**
1. Acesse **Configurações**
2. Tab **Discord**
3. Cole a URL do webhook
4. Clique em **Salvar**
5. Teste com **Testar Webhook**

**Via Terminal:**
```bash
# Edite o arquivo .env
nano .env

# Adicione:
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/SEU_ID/SEU_TOKEN
```

---

## 📊 Estrutura do Projeto

```
Projeto-coleta-financeira/
├── src/
│   ├── interface/              # Interface web
│   │   ├── app.py             # App principal
│   │   └── pages/             # Páginas da interface
│   ├── coletores/             # Coletores de dados
│   │   ├── base.py
│   │   ├── bitcoin.py
│   │   └── ethereum.py
│   ├── database/              # Gerenciamento do banco
│   │   └── db_manager.py
│   ├── utils/                 # Utilitários
│   │   ├── logger.py
│   │   └── discord_notifier.py
│   ├── pipeline.py            # Orquestrador principal
│   ├── scheduler.py           # Agendador
│   ├── alertas.py             # Sistema de alertas
│   ├── consulta.py            # Consultas CLI
│   └── dashboard.py           # Dashboard CLI
├── data/                      # Dados (SQLite + exportações)
├── logs/                      # Logs do sistema
├── tests/                     # Testes
├── .env                       # Configurações (não versionado)
├── requirements.txt           # Dependências básicas
├── requirements_web.txt       # Dependências da web
├── iniciar_interface.sh       # Script da interface
├── run_service.sh             # Gerenciar serviço
├── testar_discord.py          # Testar Discord
└── README.md                  # Este arquivo
```

---

##  Documentação

- **[COMANDOS.md](COMANDOS.md)** - Lista completa de comandos
- **[INTERFACE_WEB.md](INTERFACE_WEB.md)** - Guia da interface gráfica
- **[DISCORD_ALERTAS.md](DISCORD_ALERTAS.md)** - Configuração de alertas

---

##  Tecnologias

### Backend
- **Python 3.12+**
- **SQLite** - Banco de dados
- **Requests** - HTTP client
- **Schedule** - Agendamento
- **Pandas** - Análise de dados

### Interface Web
- **Streamlit** - Framework web
- **Plotly** - Gráficos interativos
- **Openpyxl** - Exportação Excel

### Notificações
- **Discord Webhooks** - Alertas em tempo real

---

##  Funcionalidades Detalhadas

### Coleta de Dados

- **Múltiplas Fontes:** Bitcoin, Ethereum (extensível)
- **Agendamento Flexível:** 5min a 6h de intervalo
- **Tolerância a Falhas:** Retry automático e logs
- **Execução em Background:** Serviço systemd-like

### Análise e Visualização

- **Gráficos Interativos:** Linha, candlestick, histograma, box plot
- **Estatísticas:** Média, mediana, desvio, min/max, variação
- **Comparações:** Múltiplos ativos lado a lado
- **Períodos Customizáveis:** 1 dia a histórico completo

### Sistema de Alertas

- **Variação Percentual:** Notifica quando excede limite
- **Limites de Preço:** Alertas para min/max personalizados
- **Múltiplos Canais:** Terminal, logs e Discord
- **Histórico:** Registro de todos os alertas

### Exportação

- **CSV:** Para análise em planilhas
- **JSON:** Para processamento programático
- **Excel:** Para relatórios formatados
- **Configurável:** Escolha período e quantidade

---

##  Desenvolvimento

### Adicionar Novo Coletor

1. Crie arquivo em `src/coletores/novo_ativo.py`
2. Herde de `ColetorBase`
3. Implemente `coletar()`
4. Registre em `src/pipeline.py`

```python
from coletores.base import ColetorBase

class ColetorNovoAtivo(ColetorBase):
    def __init__(self):
        super().__init__(
            nome_ativo='NOVO',
            url_api='https://api.example.com/price',
            moeda='USD'
        )

    def coletar(self):
        # Implementação específica
        pass
```

### Executar Testes

```bash
# Testar coletor individual
.venv/bin/python3 src/coletores/bitcoin.py

# Testar pipeline
.venv/bin/python3 src/pipeline.py

# Testar Discord
.venv/bin/python3 testar_discord.py
```

---

## 🐛 Solução de Problemas

### Interface não inicia

```bash
# Verificar instalação
pip list | grep streamlit

# Reinstalar
pip install -r requirements_web.txt
```

### Erro de conexão com banco

```bash
# Verificar integridade
sqlite3 data/precos_cripto.db "PRAGMA integrity_check;"

# Recriar (CUIDADO: perde dados)
rm data/precos_cripto.db
```

### Discord não envia mensagens

```bash
# Testar configuração
.venv/bin/python3 testar_discord.py

# Verificar .env
cat .env | grep DISCORD_WEBHOOK_URL
```

### Logs para debug

```bash
# Logs do pipeline
tail -f logs/pipeline.log

# Logs do scheduler
tail -f logs/scheduler.log

# Logs de alertas
tail -f logs/alertas.log
```

---

##  Exemplos de Uso

### Monitoramento Contínuo

```bash
# 1. Iniciar serviço em background
./run_service.sh start

# 2. Abrir interface web (em outro terminal)
./iniciar_interface.sh

# 3. Monitorar via dashboard
# Acesse http://localhost:8501 > Dashboard
```

### Análise Pontual

```bash
# 1. Executar coleta
.venv/bin/python3 src/pipeline.py

# 2. Consultar dados
.venv/bin/python3 src/consulta.py

# 3. Exportar análise
# Opção 6 no menu > Escolher ativo e formato
```

### Alertas Personalizados

```bash
# Via interface web
# 1. Acesse Alertas
# 2. Configure limite (ex: 5%)
# 3. Verifique automaticamente

# Via terminal
.venv/bin/python3 src/alertas.py
```

---

##  Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

---

##  Licença

Este projeto está sob licença MIT.

---

##  Roadmap

- [ ] Adicionar mais criptomoedas
- [ ] Implementar machine learning para previsões
- [ ] API REST para integração externa
- [ ] Aplicativo mobile
- [ ] Autenticação de usuários
- [ ] Dashboard público em tempo real

---

##  Suporte

- 📖 [Documentação Completa](INTERFACE_WEB.md)
- 💬 [Issues no GitHub](https://github.com/usuario/repo/issues)
- 📧 Email: suporte@exemplo.com

---

##  Agradecimentos

- Dados fornecidos por CoinGecko API
- Interface construída com Streamlit
- Gráficos powered by Plotly

---

---

##  Quick Start (TL;DR)

```bash
# Instalar
pip install -r requirements.txt
pip install -r requirements_web.txt

# Iniciar interface
./iniciar_interface.sh

# Ou via terminal
.venv/bin/python3 src/pipeline.py

# Agendar coletas
./run_service.sh start
```

**Acesse:** http://localhost:8501
