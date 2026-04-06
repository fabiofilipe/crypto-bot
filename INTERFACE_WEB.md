# Interface Gráfica Web - Guia Completo

## Visão Geral

A interface gráfica web oferece uma experiência moderna e intuitiva para gerenciar todo o sistema de coleta financeira. Construída com Streamlit, a interface permite executar todas as funcionalidades do sistema através de um navegador.

## Instalação

### 1. Instalar Dependências

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências da interface web
pip install -r requirements_web.txt
```

### 2. Iniciar a Interface

```bash
# Método 1: Usar o script de inicialização (recomendado)
./iniciar_interface.sh

# Método 2: Executar diretamente
.venv/bin/python3 -m streamlit run src/interface/app.py
```

A interface será aberta automaticamente no navegador em: **http://localhost:8501**

---

## Páginas da Interface

###  Home (Página Inicial)

**Visão Geral do Sistema**

A página inicial apresenta:

- **Cards de Métricas:**
  - Total de ativos monitorados
  - Total de registros coletados
  - Horário da última coleta

- **Resumo por Ativo:**
  - Preço atual de cada ativo
  - Estatísticas de 7 dias (mínimo, máximo, variação)
  - Total de registros

- **Status do Sistema:**
  - Conexão com banco de dados
  - Configuração do Discord
  - Status do serviço em background

- **Guia de Início Rápido:**
  - Passos para começar a usar o sistema

---

###  Dashboard

**Visualização e Análise de Dados**

#### Controles Principais

- **Seleção de Ativo:** Escolha qual criptomoeda visualizar
- **Período:** Últimas 24h, 7 dias, 30 dias ou todos os dados
- **Auto-refresh:** Atualização automática da página

#### Tabs Disponíveis

**1. Linha do Tempo**
- Gráfico interativo de evolução do preço
- Estatísticas rápidas (registros, mudança, volatilidade)
- Zoom e navegação no gráfico

**2. Estatísticas**
- Histograma de distribuição de preços
- Box plot de dispersão
- Tabela de estatísticas descritivas (média, mediana, desvio padrão, etc.)

**3. Análise Detalhada**
- Gráfico candlestick diário
- Tabela de resumo diário com variações
- Análise de tendências

**Comparação entre Ativos**
- Seleção múltipla de ativos
- Gráfico normalizado (base 100)
- Tabela comparativa de métricas

---

###  Coleta de Dados

**Execução de Coletas Manual e Automática**

#### Tab 1: Coleta Manual

**Opções de Configuração:**
- Verificar alertas (ativa/desativa)
- Limite de variação (1% a 20%)
- Enviar para Discord
- Modo detalhado

**Botões de Ação:**
1. **Executar Pipeline Completo** - Coleta todos os ativos
2. **Coletar apenas Bitcoin** - Coleta individual BTC
3. **Coletar apenas Ethereum** - Coleta individual ETH

**Status em Tempo Real:**
- Barra de progresso durante execução
- Mensagens de status de cada etapa
- Resultados detalhados após conclusão

#### Tab 2: Agendamento

**Configuração:**
- Seleção de intervalo (5, 15, 30, 60, 360 minutos)
- Instruções para iniciar via terminal
- Status do serviço em background
- Visualização de logs recentes

#### Tab 3: Histórico

**Visualização de Coletas Anteriores:**
- Seleção de ativo
- Quantidade de registros a exibir (5-100)
- Tabela com:
  - Data/Hora da coleta
  - Preço coletado
  - Variação percentual
  - Indicador de tendência (📈/📉)
- Estatísticas rápidas do período

---

###  Consultas

**Análise e Exploração de Dados**

#### Tab 1: Estatísticas

**Métricas Principais:**
- Preço atual
- Mínimo, médio e máximo do período
- Variação percentual

**Análise Detalhada:**
- Período analisado (primeira e última coleta)
- Total de registros e coletas por dia
- Amplitude de preço
- Diferença da média
- Classificação de volatilidade

**Seleção de Período:**
- 1, 7, 15, 30 ou 90 dias

#### Tab 2: Histórico Detalhado

**Tabela Completa:**
- Ordenação por data (mais recente ou mais antigo)
- Cálculo automático de variações
- Destaque colorido (verde = alta, vermelho = baixa)
- Indicadores de tendência
- Configurável até 1000 registros

**Estatísticas do Período Exibido:**
- Total de registros
- Preço médio
- Variação total
- Desvio padrão

#### Tab 3: Comparação

**Comparação Lado a Lado:**
- Seleção múltipla de ativos
- Tabela comparativa com:
  - Preço atual
  - Mínimo, médio, máximo
  - Variação percentual
  - Total de registros

**Análises Automáticas:**
- Ranking de maiores variações
- Ranking de mais coletados

#### Tab 4: Exportação

**Formatos Disponíveis:**
- CSV (com botão de download)
- JSON (com botão de download)
- Excel (salvo localmente)

**Configurações:**
- Seleção de ativo
- Limite de registros (10-10.000)
- Preview dos dados exportados
- Lista de exportações anteriores

---

###  Alertas

**Sistema de Notificações**

#### Tab 1: Verificar Alertas

**Configuração:**
- Limite de variação percentual (slider 1%-20%)
- Opção de enviar para Discord

**Modos de Verificação:**
1. **Verificar Todos os Ativos** - Análise completa
2. **Verificar Ativo Individual** - Análise específica

**Resultados:**
- Lista de alertas detectados
- Métricas de variação
- Preços anterior e atual
- Tipo de alerta (ALTA/BAIXA)

#### Tab 2: Configurar Limites

**Alertas de Preço:**
- Configuração de preço mínimo
- Configuração de preço máximo
- Verificação em tempo real
- Notificações quando limites são ultrapassados

**Recursos:**
- Visualização do preço atual
- Cálculos automáticos (sugestões de 10% acima/abaixo)
- Alertas visuais claros

#### Tab 3: Histórico

**Registro de Alertas:**
- Lista de alertas da sessão atual
- Detalhes de cada alerta:
  - Tipo de alerta
  - Ativo afetado
  - Variação ou limite
  - Horário
- Organização em expansores

---

###  Configurações

**Gerenciamento do Sistema**

#### Tab 1: Discord

**Configuração do Webhook:**
- Instruções passo a passo
- Campo seguro para URL (tipo password)
- Botão para salvar configuração
- Botão para testar webhook
- Status da configuração atual

**Funcionalidades:**
- Salva no arquivo .env
- Teste de conexão integrado
- Feedback visual de sucesso/erro

#### Tab 2: Banco de Dados

**Informações:**
- Localização do banco
- Tipo (SQLite)
- Tamanho do arquivo

**Estatísticas por Ativo:**
- Total de registros
- Primeira e última coleta
- Preço médio
- Expansores com detalhes

**Manutenção:**
- Verificar integridade (PRAGMA integrity_check)
- Otimizar banco (VACUUM e ANALYZE)

**Backup:**
- Instruções para backup manual
- Comandos de restauração

#### Tab 3: Sistema

**Informações Gerais:**
- Versão do sistema
- Versão do Python
- Estrutura de diretórios

**Logs:**
- Seleção de arquivo de log
- Configuração de linhas a exibir
- Visualização em tempo real

**Ações de Manutenção:**
- Limpar logs
- Status geral do sistema
- Informações sobre o projeto

---

## Recursos Especiais

### Gráficos Interativos

Todos os gráficos são construídos com Plotly e oferecem:

- **Zoom:** Clique e arraste para ampliar
- **Pan:** Arraste para mover
- **Hover:** Informações detalhadas ao passar o mouse
- **Download:** Botão para salvar como PNG
- **Reset:** Botão para voltar à visualização original

### Atualização em Tempo Real

- Dashboard com opção de auto-refresh
- Status do sistema atualizado automaticamente
- Indicadores visuais de carregamento

### Design Responsivo

- Interface adaptável a diferentes tamanhos de tela
- Layout otimizado para desktop e tablet
- Colunas que se reorganizam automaticamente

### Feedback Visual

-  **Sucesso:** Verde
-  **Avisos:** Amarelo/Laranja
-  **Erros:** Vermelho
-  **Informações:** Azul

---

## Atalhos e Dicas

### Navegação Rápida

Use o menu lateral para alternar entre páginas rapidamente.

### Keyboard Shortcuts (Streamlit)

- `R` - Recarregar a aplicação
- `?` - Mostrar atalhos de teclado
- `C` - Limpar cache

### Performance

Para melhor performance:
- Limite a quantidade de registros exibidos
- Use períodos menores ao visualizar gráficos
- Desative auto-refresh quando não necessário

### Exportação

- Use CSV para análises em planilhas
- Use JSON para processamento programático
- Use Excel para relatórios formatados

---

## Solução de Problemas

### Interface não abre

```bash
# Verificar se streamlit está instalado
pip list | grep streamlit

# Reinstalar se necessário
pip install streamlit
```

### Erro de módulo não encontrado

```bash
# Instalar todas as dependências
pip install -r requirements_web.txt
```

### Porta já em uso

```bash
# Usar porta diferente
streamlit run src/interface/app.py --server.port 8502
```

### Gráficos não aparecem

```bash
# Verificar se plotly está instalado
pip list | grep plotly

# Instalar se necessário
pip install plotly
```

### Dados não aparecem

1. Verifique se o banco de dados existe em `data/precos_cripto.db`
2. Execute uma coleta primeiro através da página "Coleta de Dados"
3. Verifique os logs em `logs/`

---

## Comandos Úteis

### Iniciar Interface

```bash
./iniciar_interface.sh
```

### Iniciar em Porta Diferente

```bash
streamlit run src/interface/app.py --server.port 8502
```

### Iniciar sem Abrir Navegador

```bash
streamlit run src/interface/app.py --server.headless true
```

### Acessar de Outro Dispositivo

```bash
streamlit run src/interface/app.py --server.address 0.0.0.0
```

Depois acesse: `http://IP_DO_SERVIDOR:8501`

---

## Estrutura de Arquivos

```
src/interface/
├── app.py                      # Aplicação principal
└── pages/
    ├── __init__.py
    ├── home.py                 # Página inicial
    ├── dashboard.py            # Dashboard com gráficos
    ├── coleta.py               # Coleta de dados
    ├── consultas.py            # Consultas e análises
    ├── alertas.py              # Sistema de alertas
    └── configuracoes.py        # Configurações
```

---

## Tecnologias Utilizadas

- **Streamlit** - Framework da interface web
- **Plotly** - Biblioteca de gráficos interativos
- **Pandas** - Manipulação de dados
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

---

## Próximos Passos

1. **Execute sua primeira coleta** na página "Coleta de Dados"
2. **Configure o Discord** (opcional) em "Configurações"
3. **Explore o Dashboard** para visualizar os dados
4. **Configure alertas** para ser notificado de variações

---

## Suporte

Para problemas ou sugestões:
- Verifique os logs em `logs/`
- Consulte a documentação em `COMANDOS.md`
- Revise o status do sistema em "Configurações > Sistema"

---


