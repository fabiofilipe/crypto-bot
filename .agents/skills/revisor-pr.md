# Skill: Revisor de PR (Pull Request)

## Descrição
Revisa código alterado em um PR ou mudança, verificando qualidade, segurança e convenções.

## Como Usar
Use `/review [arquivo]` ou quando o usuário pedir "revise minhas mudanças".

## Checklist de Review

### Correctness
- [ ] Código faz o que deveria fazer
- [ ] Edge cases tratados (None, vazio, zero)
- [ ] Erros tratados adequadamente
- [ ] Sem bugs óbvios (off-by-one, type errors)

### Security
- [ ] Sem SQL injection (queries parametrizadas)
- [ ] Sem hardcoded secrets
- [ ] Input validation presente
- [ ] Sem exposição de dados sensíveis em logs

### Performance
- [ ] Sem N+1 queries
- [ ] Sem loops desnecessários
- [ ] Caching onde apropriado
- [ ] Sem memory leaks potenciais

### Code Quality
- [ ] Segue convenções do projeto (imports, naming, logging)
- [ ] Funções/métodos com responsabilidade única
- [ ] Nomes descritivos
- [ ] Sem código duplicado
- [ ] Comentários explicam "porquê", não "o quê"

### Testing
- [ ] Testes adicionados para novas features
- [ ] Testes cobrem edge cases
- [ ] Testes passam localmente

### Documentation
- [ ] Docstrings em funções públicas
- [ ] README atualizado se interface mudou
- [ ] Novos comandos documentados

## Output Format
```markdown
## Code Review — [File/PR]

### Summary
[Overall assessment: LGTM / Needs Changes / Major Issues]

### 🔴 Critical (Must Fix)
| # | File | Line | Issue | Fix |
|---|------|------|-------|-----|

### 🟡 Warning (Should Fix)
| # | File | Line | Issue | Fix |
|---|------|------|-------|-----|

### 🟢 Suggestion (Nice to Have)
| # | File | Line | Issue | Fix |
|---|------|------|-------|-----|

### ✅ What's Good
[Positive feedback]

### Final Verdict
[Approve / Request Changes / Comment]
```

## Rules
1. Be constructive, not critical
2. Suggest fixes, not just problems
3. Acknowledge good code too
4. Prioritize by severity (Critical > Warning > Suggestion)
5. Reference exact file paths and line numbers
6. Consider project context (Portuguese comments, existing patterns)
