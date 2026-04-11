# Workflows Encadeados — Sistema de Coleta Financeira

Workflows complexos que encadeiam múltiplos agentes e skills para tarefas completas.

---

## Workflow 1: Implementar Feature Completa

**Trigger:** "Implemente [feature]"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. architect → Design da feature                       │
│     ↓                                                    │
│  2. feature-builder → Implementa                        │
│     ↓                                                    │
│  3. test-engineer → Escreve testes                      │
│     ↓                                                    │
│  4. security-auditor → Revisão de segurança             │
│     ↓                                                    │
│  5. code-analyst → Review de qualidade                  │
│     ↓                                                    │
│  6. ui-reviewer → Review de UX (se afeta UI/Discord)    │
│     ↓                                                    │
│  7. ORQUESTRADOR → Verifica tudo e consolida             │
└─────────────────────────────────────────────────────────┘
```

**Exemplo:**
```
User: "Implemente alerta por usuário no Discord"

Orchestrator delega:
1. architect → Design: tabela alertas_config já existe, 
   como integrar com SistemaAlertas?
2. feature-builder → Modifica alertas.py, db_manager.py, 
   bot_discord.py (comando !alerta-config)
3. test-engineer → Testes: verificar_alert, configurar_alerta, 
   mock db, mock discord_notifier
4. security-auditor → Validar: usuário só configura seus próprios alertas?
5. ui-reviewer → Revisar: comandos do bot são claros? 
   Interface web de alertas atualizada?
6. orchestrator → Consolidar: sumarizar mudanças, 
   verificar testes passando, docs atualizadas
```

---

## Workflow 2: Preparar para Produção

**Trigger:** "Prepare o projeto para produção"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. security-auditor → Audit completa                    │
│     ↓                                                    │
│  2. bug-fixer → Corrige issues críticas/altas            │
│     ↓                                                    │
│  3. test-engineer → Cria testes do caminho crítico       │
│     ↓                                                    │
│  4. devops-engineer → Docker + CI/CD                     │
│     ↓                                                    │
│  5. db-specialist → Otimiza DB + retenção de dados       │
│     ↓                                                    │
│  6. scaling-engineer → Analisa gargalos                  │
│     ↓                                                    │
│  7. architect → Review final de arquitetura              │
│     ↓                                                    │
│  8. ORQUESTRADOR → Checklist de produção                  │
└─────────────────────────────────────────────────────────┘
```

**Checklist de Produção:**
- [ ] Zero vulnerabilidades críticas/altas
- [ ] Testes do caminho crítico passando
- [ ] Docker otimizado, non-root user
- [ ] CI/CD configurado (lint → test → build)
- [ ] DB com retenção de dados
- [ ] Healthchecks em todos services
- [ ] Logs com rotação
- [ ] .env.example atualizado
- [ ] README com instruções de deploy
- [ ] Monitoring/alerting do sistema

---

## Workflow 3: Adicionar Nova Exchange (Binance)

**Trigger:** "Adicione suporte à Binance"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. architect → Design: wrapper API + collector pattern  │
│     ↓                                                    │
│  2. feature-builder → binance_api.py + coletor           │
│     ↓                                                    │
│  3. feature-builder → Integra com pipeline (fallback)    │
│     ↓                                                    │
│  4. test-engineer → Testes: mocks de API, retry, error   │
│     ↓                                                    │
│  5. security-auditor → API keys, secrets, rate limits    │
│     ↓                                                    │
│  6. scaling-engineer → Performance: parallel vs fallback │
│     ↓                                                    │
│  7. ORQUESTRADOR → E2E test: coleta Binance → DB         │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 4: Corrigir Bug + Prevenir Regressão

**Trigger:** "Corrija [bug] e evite que aconteça de novo"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. bug-fixer → Diagnostica e corrige bug                │
│     ↓                                                    │
│  2. test-engineer → Teste de regressão                   │
│     ↓                                                    │
│  3. code-analyst → Busca padrões similares no codebase   │
│     ↓                                                    │
│  4. bug-fixer → Corrige todas as instâncias similares    │
│     ↓                                                    │
│  5. test-engineer → Roda todos os testes                 │
│     ↓                                                    │
│  6. ORQUESTRADOR → Verifica bug resolvido + testes       │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 5: Refatorar Módulo

**Trigger:** "Refatore [módulo]"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. code-analyst → Análise atual: métricas, smells       │
│     ↓                                                    │
│  2. architect → Design melhorado: padrões, estrutura     │
│     ↓                                                    │
│  3. feature-builder → Implementa refatoração             │
│     ↓                                                    │
│  4. test-engineer → Atualiza/cria testes                 │
│     ↓                                                    │
│  5. code-analyst → Análise pós-refatoração               │
│     ↓                                                    │
│  6. security-auditor → Verifica regressões de segurança  │
│     ↓                                                    │
│  7. ORQUESTRADOR → Compara antes/depois                  │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 6: Audit e Correção de Segurança

**Trigger:** "Audite a segurança do projeto"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. security-auditor → Audit completo (checklist)        │
│     ↓                                                    │
│  2. bug-fixer → Corrige vulnerabilidades críticas/altas  │
│     ↓                                                    │
│  3. test-engineer → Testes de segurança (injection, etc) │
│     ↓                                                    │
│  4. security-auditor → Re-audit para verificar correções │
│     ↓                                                    │
│  5. devops-engineer → Hardening de Docker/infra          │
│     ↓                                                    │
│  6. ORQUESTRADOR → Relatório final de segurança           │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 7: Otimizar Performance

**Trigger:** "Otimize a performance do sistema"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. scaling-engineer → Identifica gargalos (mede)        │
│     ↓                                                    │
│  2. db-specialist → Otimiza queries, indexes, pooling    │
│     ↓                                                    │
│  3. feature-builder → Implementa caching, parallelismo   │
│     ↓                                                    │
│  4. scaling-engineer → Mede melhoria (antes/depois)      │
│     ↓                                                    │
│  5. test-engineer → Testes de carga/performance          │
│     ↓                                                    │
│  6. ORQUESTRADOR → Relatório de performance               │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 8: Review de UI/UX Completo

**Trigger:** "Melhore a experiência do usuário"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. ui-reviewer → Audit UI: Streamlit + Discord embeds   │
│     ↓                                                    │
│  2. feature-builder → Implementa melhorias de UI         │
│     ↓                                                    │
│  3. ui-reviewer → Verifica melhorias                     │
│     ↓                                                    │
│  4. test-engineer → E2E tests com Playwright MCP         │
│     ↓                                                    │
│  5. ORQUESTRADOR → Before/after summary                   │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 9: Setup CI/CD Completo

**Trigger:** "Configure CI/CD com GitHub Actions"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. devops-engineer → Cria .github/workflows/ci.yml      │
│     ↓                                                    │
│  2. test-engineer → Garante que testes estão prontos     │
│     ↓                                                    │
│  3. devops-engineer → Configura Docker build + push       │
│     ↓                                                    │
│  4. security-auditor → Scan de vulnerabilidades (Trivy)  │
│     ↓                                                    │
│  5. devops-engineer → Configura auto-deploy              │
│     ↓                                                    │
│  6. ORQUESTRADOR → Testa pipeline com push de teste       │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow 10: Onboarding de Novo Desenvolvedor

**Trigger:** "Configure o ambiente para um novo dev"

```
┌─────────────────────────────────────────────────────────┐
│                    ORQUESTRADOR                          │
│                                                          │
│  1. setup-rapido (skill) → Ambiente base                 │
│     ↓                                                    │
│  2. code-analyst → Explica arquitetura do projeto        │
│     ↓                                                    │
│  3. architect → Visão geral do sistema e decisões        │
│     ↓                                                    │
│  4. ORQUESTRADOR → Checklist de onboarding completo       │
└─────────────────────────────────────────────────────────┘
```

---

## Como Usar Workflows

1. **Identifique o tipo de tarefa** — Match com um dos workflows acima
2. **Invoque o orquestrador** — `agent(general-purpose)` com o prompt do orchestrator.md
3. **Orquestrador delega** — Ele usa os agentes especializados em sequência
4. **Verifique o resultado** — Orquestrador consolida tudo no final

### Exemplo de Uso

```
User: "Implemente alertas configuráveis por usuário no Discord"

Qwen (como orquestrador):
1. Lê .agents/orquestracao/orchestrator.md
2. Identifica: Workflow 1 (Feature Completa)
3. Delega: architect → feature-builder → test-engineer → security → code-analyst → ui-reviewer
4. Consolida resultado final
```
