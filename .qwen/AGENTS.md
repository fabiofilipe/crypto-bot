# Guia de Agentes e Skills — Sistema de Coleta Financeira

Este documento explica como usar os agentes e skills customizados **nativamente integrados** ao Qwen Code.

---

## Estrutura

```
.qwen/
├── settings.json                    → MCP servers (postgres, docker, playwright, etc.)
├── agents/                          → 11 subagents oficiais com YAML frontmatter
│   ├── code-analyst.md
│   ├── bug-fixer.md
│   ├── security-auditor.md
│   ├── feature-builder.md
│   ├── test-engineer.md
│   ├── devops-engineer.md
│   ├── db-specialist.md
│   ├── architect.md
│   ├── scaling-engineer.md
│   ├── ui-reviewer.md
│   └── orchestrator.md
├── skills/                          → 4 skills oficiais com SKILL.md
│   ├── gerador-testes/SKILL.md
│   ├── adicionar-cripto/SKILL.md
│   ├── revisor-pr/SKILL.md
│   └── setup-rapido/SKILL.md
├── AGENTS.md                        ← Este arquivo
├── PROMPTS.md                       → Templates de prompts
└── REFERENCE.md                     → Cartão de referência rápida

.agents/                             → Referência adicional (catálogo humano, workflows)
├── INDICE.md                        → Índice mestre de tudo
└── workflows/workflows-encadeados.md → 10 workflows detalhados
```

---

## Como Usar — 3 Níveis

### Nível 1: Automático (Natural Language)

O Qwen **auto-dispatcha** para o agente/skill correto baseado na sua linguagem natural:

```
"Analise a qualidade do código em src/bot_discord.py"    → code-analyst
"Corrija o bug no comando !comparar"                      → bug-fixer
"Crie testes para o sistema de alertas"                   → test-engineer
"Adicione PEPE ao sistema"                                → adicionar-cripto (skill)
```

### Nível 2: Explícito (Nome do Agente)

Você pode invocar diretamente pelo nome:

```
"Use o code-analyst para avaliar src/alertas.py"
"Use o bug-fixer para corrigir o erro de conexão"
"Use o test-engineer para criar testes do db_manager"
```

### Nível 3: Workflow (Orquestrador)

Para tarefas complexas:

```
"Implemente suporte à Binance"           → orchestrator delega multi-agente
"Prepare o projeto para produção"        → orchestrator executa workflow completo
```

---

## 11 Agents Disponíveis

| Agente | Quando Chamar |
|--------|---------------|
| **code-analyst** | "Analise qualidade do código", "Encontre code smells" |
| **bug-fixer** | "Corrija o bug em X", "Erro ao rodar Y" |
| **security-auditor** | "Audite a segurança", "Verifique SQL injection" |
| **feature-builder** | "Implemente X", "Adicione feature Y", "Crie Z" |
| **test-engineer** | "Crie testes para X", "Configure coverage" |
| **devops-engineer** | "Otimize Docker", "Configure CI/CD", "Container não inicia" |
| **db-specialist** | "Otimize queries", "Crie migração", "Analise performance DB" |
| **architect** | "Como escalar?", "Brainstorm de ideias", "Devemos mudar para X?" |
| **scaling-engineer** | "Otimize performance", "Escale para X cryptos" |
| **ui-reviewer** | "Melhore a UI", "Revise UX do dashboard", "Melhore embeds Discord" |
| **orchestrator** | Tarefas complexas multi-agente: "implemente X completo" |

---

## 4 Skills Disponíveis

| Skill | Quando Chamar |
|-------|---------------|
| **gerador-testes** | "Crie testes para [módulo]" |
| **adicionar-cripto** | "Adicione [CRYPTO] ao sistema" |
| **revisor-pr** | "Revise minhas mudanças" |
| **setup-rapido** | "Configure meu ambiente" |

---

## 5 MCP Servers Configurados

| MCP | Para Quê |
|-----|----------|
| **postgres** | Query dados de criptomoedas coletados |
| **docker** | Gerenciar containers (status, logs, restart) |
| **playwright** | Testar interface Streamlit, screenshots E2E |
| **git** | History, blame, diff analysis |
| **filesystem** | Navegar projeto, operações de arquivo |

---

## Workflows Encadeados

Veja `.agents/workflows/workflows-encadeados.md` para os 10 workflows detalhados.

| # | Workflow | Agentes Envolvidos |
|---|----------|-------------------|
| 1 | Implementar Feature | architect → builder → tests → security → analyst → ui |
| 2 | Preparar Produção | security → bug-fixer → tests → devops → db → scaling → architect |
| 3 | Adicionar Exchange | architect → builder → tests → security → scaling |
| 4 | Corrigir + Prevenir | bug-fixer → tests → analyst → bug-fixer |
| 5 | Refatorar Módulo | analyst → architect → builder → tests → security |
| 6 | Audit Segurança | security → bug-fixer → tests → security → devops |
| 7 | Otimizar Performance | scaling → db → builder → scaling → tests |
| 8 | Review UI/UX | ui-reviewer → builder → ui-reviewer → tests |
| 9 | Setup CI/CD | devops → tests → devops → security → devops |
| 10 | Onboarding Dev | setup → analyst → architect |

---

## Exemplos Práticos

### Simples (1 agente)
```
"Use o db-specialist para otimizar as queries do db_manager"
```

### Com skill
```
"Use o skill adicionar-cripto para adicionar PEPE"
```

### Workflow (orquestrador)
```
"Implemente alertas por usuário no Discord"
→ O orchestrator identifica Workflow 1
→ architect → feature-builder → test-engineer → security-auditor → code-analyst
→ Resultado consolidado
```

### Com MCP
```
"Use o postgres MCP para mostrar as últimas 10 coletas de BTC"
"Use o playwright MCP para abrir localhost:8501 e screenshot a home"
```

---

## Notas Importantes

1. **Agents** (`.qwen/agents/`) são **auto-descobertos** pelo Qwen Code via YAML frontmatter
2. **Skills** (`.qwen/skills/*/SKILL.md`) são **auto-descobertos** pelo Qwen Code
3. **`.agents/`** é referência adicional — útil como catálogo humano e workflows detalhados, mas **não** é auto-carregado nativamente
4. O Qwen Code escolhe automaticamente o agente certo baseado na descrição do seu pedido
