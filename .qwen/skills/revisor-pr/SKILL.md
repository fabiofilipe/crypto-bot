---
name: revisor-pr
description: Revisa código alterado verificando correctness, security, performance, code quality e testes. Use para "revise minhas mudanças" ou junto com /review.
---

## Checklist
- **Correctness**: Código faz que deveria? Edge cases? Erros tratados?
- **Security**: SQL injection? Hardcoded secrets? Input validation?
- **Performance**: N+1 queries? Loops desnecessários? Caching?
- **Code Quality**: Convenções do projeto? Nomes descritivos? Sem duplicação?
- **Testing**: Testes adicionados? Cobrem edge cases? Passam?
- **Documentation**: Docstrings? README atualizado? Comandos documentados?

## Output
```
## Code Review — [Arquivo]

### 🔴 Critical (Must Fix)
### 🟡 Warning (Should Fix)
### 🟢 Suggestion (Nice to Have)
### ✅ What's Good

### Verdict: Approve / Request Changes
```

## Regras
- Construtivo, não crítico
- Sugira fixes, não só problemas
- Reconheça bom código também
- Referencie arquivos e linhas exatos
