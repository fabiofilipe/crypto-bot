# Guia de Comandos - Sistema de Coleta Financeira

Este documento lista todos os comandos disponíveis no sistema de coleta de dados financeiros.

## Sumário

1. [Coleta de Dados](#coleta-de-dados)
2. [Consultas e Análises](#consultas-e-análises)
3. [Monitoramento](#monitoramento)
4. [Alertas](#alertas)
5. [Serviço em Background](#serviço-em-background)
6. [Migração de Dados](#migração-de-dados)
7. [Coletores Individuais](#coletores-individuais)

---

## Coleta de Dados

### Pipeline Completo (Execução Única)

Executa todos os coletores uma única vez:

```bash
.venv/bin/python3 src/pipeline.py
```

**O que faz:**
- Coleta dados de Bitcoin e Ethereum
- Salva no banco de dados SQLite
- Verifica alertas de variação de preço
- Envia notificações para Discord (se configurado)
- Mostra relatório de execução

---

### Agendador Automático

Executa coletas em intervalos programados:

```bash
.venv/bin/python3 src/scheduler.py
```

**Opções de intervalo:**
1. A cada 5 minutos (para testes)
2. A cada 15 minutos
3. A cada 30 minutos (recomendado)
4. A cada 1 hora
5. A cada 6 horas
6. Personalizado (você escolhe o intervalo)

**O que faz:**
- Executa o pipeline automaticamente
- Mostra contagem regressiva para próxima execução
- Registra logs de todas as execuções
- Continua rodando até pressionar Ctrl+C

---

## Consultas e Análises

### Sistema de Consultas Interativo

Menu interativo para explorar os dados coletados:

```bash
.venv/bin/python3 src/consulta.py
```

**Funcionalidades disponíveis:**

#### 1. Listar ativos disponíveis
- Mostra todos os ativos no banco
- Exibe quantidade de registros de cada um

#### 2. Ver último preço
- Consulta o preço mais recente de um ativo
- Mostra horário da última coleta

#### 3. Ver estatísticas
- Preço mínimo, médio e máximo
- Variação percentual no período
- Data da primeira e última coleta
- Configurável (1, 7, 30 dias, etc.)

#### 4. Ver histórico
- Lista preços recentes
- Quantidade de registros configurável
- Mostra evolução temporal

#### 5. Comparar ativos
- Compara múltiplos ativos simultaneamente
- Mostra estatísticas lado a lado
- Útil para análise de correlação

#### 6. Exportar para CSV
- Exporta dados para arquivo CSV
- Configurável quantidade de registros
- Arquivo salvo em `data/exportacao_*.csv`

---

## Monitoramento

### Dashboard em Tempo Real

Dashboard visual no terminal com atualização automática:

```bash
.venv/bin/python3 src/dashboard.py
```

**Opções de atualização:**
1. A cada 5 segundos (atualização rápida)
2. A cada 10 segundos (recomendado)
3. A cada 30 segundos
4. A cada 60 segundos

**Informações exibidas:**
- Preço atual de todos os ativos
- Estatísticas do dia (min, max, média, variação)
- Estatísticas da semana
- Quantidade de coletas realizadas
- Horário da última atualização
- Cores indicativas (verde para alta, vermelho para baixa)

---

## Alertas

### Sistema de Alertas Manual

Verifica variações de preço manualmente:

```bash
.venv/bin/python3 src/alertas.py
```

**O que faz:**
- Verifica variações em todos os ativos
- Configura limites de variação percentual (padrão: 3%)
- Envia notificações no terminal + Discord
- Pode configurar limites de preço (mínimo/máximo)

### Testar Integração Discord

Testa se os alertas estão chegando no Discord:

```bash
.venv/bin/python3 testar_discord.py
```

**O que faz:**
- Testa conexão com webhook do Discord
- Envia 6 mensagens de teste:
  - Alerta de variação para ALTA
  - Alerta de variação para BAIXA
  - Alerta de preço abaixo do mínimo
  - Alerta de preço acima do máximo
  - Mensagem simples
  - Mensagem de teste de conexão

---

## Serviço em Background

### Gerenciar Serviço

Script para executar o scheduler como serviço em background:

#### Iniciar serviço

```bash
./run_service.sh start
```

Inicia o agendador em background, salvando logs em `logs/service.log`

#### Parar serviço

```bash
./run_service.sh stop
```

Para a execução do serviço em background

#### Verificar status

```bash
./run_service.sh status
```

Mostra se o serviço está rodando e exibe últimas linhas do log

#### Reiniciar serviço

```bash
./run_service.sh restart
```

Para e inicia novamente o serviço

---

## Migração de Dados

### Migrar CSVs para SQLite

Importa dados de arquivos CSV para o banco de dados:

```bash
.venv/bin/python3 src/migrar_csv.py
```

**O que faz:**
- Busca todos os arquivos `preco_*.csv` em `data/raw/`
- Valida estrutura dos CSVs
- Insere dados no banco SQLite
- Mostra resumo da migração
- Lista estatísticas após migração

**Formato esperado do CSV:**
```csv
ativo,preco,moeda,horario_coleta
BTC,67500.00,USD,2025-01-15 10:30:00
```

---

## Coletores Individuais

### Coletor de Bitcoin

Executa apenas coleta de Bitcoin:

```bash
.venv/bin/python3 src/coletores/bitcoin.py
```

### Coletor de Ethereum

Executa apenas coleta de Ethereum:

```bash
.venv/bin/python3 src/coletores/ethereum.py
```

**Uso dos coletores individuais:**
- Útil para testes
- Debug de problemas específicos
- Validação de APIs
- Desenvolvimento de novos coletores

---

## Comandos Auxiliares

### Visualizar Logs

#### Log do pipeline
```bash
tail -f logs/pipeline.log
```

#### Log do scheduler
```bash
tail -f logs/scheduler.log
```

#### Log de alertas
```bash
tail -f logs/alertas.log
```

#### Log do serviço em background
```bash
tail -f logs/service.log
```

### Limpar Banco de Dados

**CUIDADO:** Este comando remove todos os dados!

```bash
rm data/precos_cripto.db
# O banco será recriado automaticamente na próxima execução
```

### Verificar Estrutura do Banco

```bash
sqlite3 data/precos_cripto.db ".schema"
```

### Contar Registros

```bash
sqlite3 data/precos_cripto.db "SELECT ativo, COUNT(*) as total FROM precos GROUP BY ativo;"
```

---

## Fluxo de Trabalho Recomendado

### 1. Primeira Execução

```bash
# 1. Testar conectividade
.venv/bin/python3 src/coletores/bitcoin.py

# 2. Executar pipeline completo
.venv/bin/python3 src/pipeline.py

# 3. Verificar dados coletados
.venv/bin/python3 src/consulta.py
```

### 2. Configurar Discord (Opcional)

```bash
# 1. Editar .env com a URL do webhook
nano .env

# 2. Testar integração
.venv/bin/python3 testar_discord.py
```

### 3. Iniciar Monitoramento

```bash
# Opção 1: Dashboard interativo (terminal dedicado)
.venv/bin/python3 src/dashboard.py

# Opção 2: Serviço em background
./run_service.sh start
```

### 4. Análise de Dados

```bash
# Consultas interativas
.venv/bin/python3 src/consulta.py

# Ou exportar para análise externa
# (escolher opção 6 no menu de consultas)
```

---

## Atalhos Úteis

### Execução Rápida (sem entrar no venv)

Todos os comandos podem ser executados diretamente usando:

```bash
.venv/bin/python3 src/<script>.py
```

### Ver Todos os Ativos Rapidamente

```bash
sqlite3 data/precos_cripto.db "SELECT DISTINCT ativo FROM precos;"
```

### Última Coleta de Cada Ativo

```bash
sqlite3 data/precos_cripto.db "
SELECT ativo, preco, moeda, horario_coleta
FROM precos
GROUP BY ativo
HAVING id = MAX(id)
ORDER BY ativo;
"
```

---

## Solução de Problemas

### Erro: "Module not found"

```bash
# Garantir que está usando o Python do venv
.venv/bin/python3 src/pipeline.py
```

### Discord não recebe mensagens

```bash
# 1. Verificar se .env está configurado
cat .env

# 2. Testar webhook
.venv/bin/python3 testar_discord.py
```

### Serviço não inicia

```bash
# 1. Verificar logs
cat logs/service.log

# 2. Remover PID antigo se necessário
rm pipeline.pid

# 3. Tentar iniciar novamente
./run_service.sh start
```

### Banco de dados corrompido

```bash
# 1. Fazer backup
cp data/precos_cripto.db data/precos_cripto.db.backup

# 2. Tentar reparar
sqlite3 data/precos_cripto.db "PRAGMA integrity_check;"

# 3. Se necessário, recriar
rm data/precos_cripto.db
.venv/bin/python3 src/pipeline.py
```

---

## Configurações Avançadas

### Alterar Intervalo do Scheduler Programaticamente

Edite `src/scheduler.py` linha 116:

```python
agendador.agendar(intervalo_minutos=15)  # Altere aqui
```

### Adicionar Novo Ativo

1. Crie novo coletor em `src/coletores/`
2. Registre no pipeline em `src/pipeline.py` linha 17-20

### Alterar Limite de Alertas

No `src/pipeline.py` linha 16:

```python
def __init__(self, habilitar_alertas=True, limite_variacao=3.0):  # Altere limite_variacao
```

---

## Referências Rápidas

| Comando | Descrição |
|---------|-----------|
| `src/pipeline.py` | Coleta única |
| `src/scheduler.py` | Coleta automática |
| `src/consulta.py` | Menu de consultas |
| `src/dashboard.py` | Dashboard visual |
| `src/alertas.py` | Verificar alertas |
| `testar_discord.py` | Testar Discord |
| `run_service.sh start` | Iniciar serviço |
| `run_service.sh status` | Ver status |

---

**Dica:** Mantenha este arquivo aberto durante o uso do sistema para referência rápida!

📝 Consultas SQL Diretas

  # Ver todos os ativos
  sqlite3 data/precos_cripto.db "SELECT DISTINCT ativo FROM precos;"

  # Contar registros por ativo
  sqlite3 data/precos_cripto.db "SELECT ativo, COUNT(*) FROM precos GROUP BY ativo;"

  # Último preço de cada ativo
  sqlite3 data/precos_cripto.db "SELECT ativo, preco, moeda, horario_coleta FROM precos GROUP BY ativo 
  HAVING id = MAX(id);"