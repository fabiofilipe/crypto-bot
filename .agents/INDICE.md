# Índice Mestre de Agentes — Sistema de Coleta Financeira

Visão centralizada de todos os agentes, skills e workflows disponíveis.

---

## 📂 Estrutura de Diretórios

```
.agents/
├── analise/
│   └── code-analyst.md          → Analista de Código
├── correcao/
│   └── bug-fixer.md             → Corretor de Bugs
├── seguranca/
│   └── security-auditor.md      → Auditor de Segurança
├── implementacao/
│   └── feature-builder.md       → Construtor de Features
├── testes/
│   └── test-engineer.md         → Engenheiro de Testes
├── devops/
│   └── devops-engineer.md       → Engenheiro DevOps
├── database/
│   └── db-specialist.md         → Especialista em Banco de Dados
├── arquitetura/
│   └── architect.md             → Arquiteto/Brainstorm
├── orquestracao/
│   └── orchestrator.md          → Orquestrador de Tarefas
├── escalabilidade/
│   └── scaling-engineer.md      → Engenheiro de Escalabilidade
├── ui-ux/
│   └── ui-reviewer.md           → Revisor de UI/UX
├── skills/
│   ├── gerador-testes-rapidos.md → Skill: Gerar testes automaticamente
│   ├── adicionar-cripto.md       → Skill: Adicionar nova cripto
│   ├── revisor-pr.md             → Skill: Revisar PR/mudanças
│   └── setup-rapido.md           → Skill: Setup de ambiente
└── workflows/
    └── workflows-encadeados.md   → 10 workflows prontos
```

---

## 🤖 Agentes Disponíveis

| # | Agente | Arquivo | Quando Usar |
|---|--------|---------|-------------|
| 1 | **code-analyst** | `analise/code-analyst.md` | "Analise a qualidade do código", "Encontre code smells" |
| 2 | **bug-fixer** | `correcao/bug-fixer.md` | "Corrija o bug em X", "Erro ao rodar Y" |
| 3 | **security-auditor** | `seguranca/security-auditor.md` | "Audite a segurança", "Verifique SQL injection" |
| 4 | **feature-builder** | `implementacao/feature-builder.md` | "Implemente X", "Adicione feature Y" |
| 5 | **test-engineer** | `testes/test-engineer.md` | "Crie testes para X", "Configure coverage" |
| 6 | **devops-engineer** | `devops/devops-engineer.md` | "Otimize Docker", "Configure CI/CD" |
| 7 | **db-specialist** | `database/db-specialist.md` | "Otimize queries", "Crie migração de DB" |
| 8 | **architect** | `arquitetura/architect.md` | "Como escalar?", "Brainstorm de ideias" |
| 9 | **orchestrator** | `orquestracao/orchestrator.md` | Tarefas complexas com múltiplos passos |
| 10 | **scaling-engineer** | `escalabilidade/scaling-engineer.md` | "Otimize performance", "Escale para X" |
| 11 | **ui-reviewer** | `ui-ux/ui-reviewer.md` | "Melhore a UI", "Revise UX do dashboard" |

---

## 🔧 Skills Disponíveis

| # | Skill | Arquivo | Quando Usar |
|---|-------|---------|-------------|
| 1 | **gerador-testes-rapidos** | `skills/gerador-testes-rapidos.md` | "Crie testes para [módulo]" |
| 2 | **adicionar-cripto** | `skills/adicionar-cripto.md` | "Adicione [CRYPTO] ao sistema" |
| 3 | **revisor-pr** | `skills/revisor-pr.md` | "Revise minhas mudanças", `/review` |
| 4 | **setup-rapido** | `skills/setup-rapido.md` | "Configure meu ambiente" |

---

## 🔄 Workflows Encadeados

| # | Workflow | Quando Usar | Agentes Envolvidos |
|---|----------|-------------|-------------------|
| 1 | **Implementar Feature Completa** | "Implemente [feature]" | architect → feature-builder → test-engineer → security → code-analyst → ui-reviewer |
| 2 | **Preparar para Produção** | "Prepare para produção" | security → bug-fixer → tests → devops → db → scaling → architect |
| 3 | **Adicionar Nova Exchange** | "Adicione Binance" | architect → feature-builder → tests → security → scaling |
| 4 | **Corrigir Bug + Prevenir** | "Corrija e previna" | bug-fixer → tests → code-analyst → bug-fixer |
| 5 | **Refatorar Módulo** | "Refatore [módulo]" | code-analyst → architect → feature-builder → tests → security |
| 6 | **Audit de Segurança** | "Audite segurança" | security → bug-fixer → tests → security → devops |
| 7 | **Otimizar Performance** | "Otimize performance" | scaling → db → feature-builder → scaling → tests |
| 8 | **Review de UI/UX** | "Melhore UX" | ui-reviewer → feature-builder → ui-reviewer → tests |
| 9 | **Setup CI/CD** | "Configure CI/CD" | devops → tests → devops → security → devops |
| 10 | **Onboarding de Dev** | "Novo desenvolvedor" | setup → code-analyst → architect |

---

## 🚀 Como Usar

### Uso Simples (1 Agente)
```
User: "Analise a qualidade do código em src/bot_discord.py"

Qwen:
1. Lê .agents/analise/code-analyst.md
2. Usa o checklist e output format do agente
3. Retorna análise completa
```

### Uso com Skill
```
User: "Adicione PEPE ao sistema"

Qwen:
1. Lê .agents/skills/adicionar-cripto.md
2. Segue o processo passo a passo
3. Valida e reporta resultado
```

### Uso com Workflow (Orquestrador)
```
User: "Implemente suporte à Binance"

Qwen (como orquestrador):
1. Lê .agents/orquestracao/orchestrator.md
2. Identifica Workflow 3 (Adicionar Exchange)
3. Delega para cada agente em sequência
4. Consolida resultado final
```

---

## 📋 Matriz de Decisão Rápida

| Se você quer... | Use... | Tipo |
|-----------------|--------|------|
| Entender código | code-analyst | Agente |
| Corrigir erro | bug-fixer | Agente |
| Verificar segurança | security-auditor | Agente |
| Criar feature | feature-builder | Agente |
| Escrever testes | test-engineer | Agente |
| Configurar infra | devops-engineer | Agente |
| Otimizar DB | db-specialist | Agente |
| Planejar arquitetura | architect | Agente |
| Tarefa complexa | orchestrator | Agente |
| Escalar sistema | scaling-engineer | Agente |
| Melhorar UI | ui-reviewer | Agente |
| Testes rápidos | gerador-testes-rapidos | Skill |
| Adicionar cripto | adicionar-cripto | Skill |
| Revisar mudanças | revisor-pr | Skill |
| Setup ambiente | setup-rapido | Skill |
| Feature completa | Workflow 1 | Workflow |
| Ir para produção | Workflow 2 | Workflow |
| Nova exchange | Workflow 3 | Workflow |
| Corrigir + prevenir | Workflow 4 | Workflow |
| Refatorar | Workflow 5 | Workflow |
| Audit segurança | Workflow 6 | Workflow |
| Performance | Workflow 7 | Workflow |
| Review UI/UX | Workflow 8 | Workflow |
| CI/CD | Workflow 9 | Workflow |
| Onboarding | Workflow 10 | Workflow |

---

## 🎯 Exemplos Práticos de Uso

### Exemplo 1: Análise Rápida
```
Prompt: "Use o code-analyst para avaliar src/alertas.py"
Agente: code-analyst
Output: Métricas, code smells, recomendações
```

### Exemplo 2: Correção de Bug
```
Prompt: "O comando !comparar está falhando. Use o bug-fixer."
Agente: bug-fixer
Output: Root cause, fix aplicado, teste de regressão
```

### Exemplo 3: Feature Completa
```
Prompt: "Implemente alertas por usuário no Discord"
Workflow: 1 (Feature Completa)
Agentes: architect → feature-builder → test-engineer → security → code-analyst
Output: Feature implementada, testada, auditada, documentada
```

### Exemplo 4: Produção
```
Prompt: "Prepare o projeto para ir para produção"
Workflow: 2 (Preparar para Produção)
Agentes: security → bug-fixer → tests → devops → db → scaling → architect
Output: Checklist de produção completo, zero issues críticas
```

---

## ⚙️ Integração com MCP

| MCP Server | Agente que Mais Usa | Para Quê |
|------------|---------------------|----------|
| postgres | db-specialist | Queries, otimização, migrações |
| docker | devops-engineer | Build, status, logs, optimization |
| playwright | ui-reviewer | E2E testing, screenshots, UX validation |
| git | todos | History, blame, diff analysis |
| filesystem | todos | Navigation, file operations |

---

## 📊 Estatísticas do Projeto (Contexto para Agentes)

| Métrica | Valor |
|---------|-------|
| Arquivos Python | 27 |
| Linhas de Código (estimado) | ~5,000+ |
| Cryptos Monitoradas | 12 |
| Comandos Discord | 9 (+ aliases) |
| Páginas Streamlit | 6 |
| Testes Existentes | 0 (roadmap) |
| CI/CD | Não configurado |
| Exchanges | 1 (Coinbase) |
| Serviços Docker | 4 |

---

## 🔄 Atualização

Este índice deve ser atualizado quando:
- Novo agente criado
- Agente removido ou renomeado
- Novo workflow adicionado
- Skill adicionado
- Estrutura de diretórios muda
