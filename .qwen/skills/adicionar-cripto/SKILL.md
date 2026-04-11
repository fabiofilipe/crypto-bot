---
name: adicionar-cripto
description: Adiciona uma nova criptomoeda ao sistema de coleta de forma rápida e segura. Use para "adicione [CRYPTO] ao sistema".
---

## Processo
1. Leia src/pipeline.py para encontrar ATIVOS_DISPONIVEIS
2. Adicione novo ativo: `("NOVO", "NomeDaCripto")`
3. Atualize aliases em bot_discord.py (_resolver_ativo): `"NOME": "NOVO", "NOVO": "NOVO"`
4. Teste coleta individual: `ColetorDinamico(simbolo="NOVO", nome="Nome").executar()`
5. Verifique no banco: `SELECT * FROM precos WHERE ativo = 'NOVO'`

## Validação
- [ ] Ativo em ATIVOS_DISPONIVEIS
- [ ] Aliases em _resolver_ativo
- [ ] Coleta individual funciona
- [ ] Registro no banco
- [ ] Comando Discord: !crypto NOVO

## Rollback
Se falhar, remova a linha em ATIVOS_DISPONIVEIS e aliases.
Nota: Coinbase deve suportar o par {simbolo}-USD ou coleta falhará com 404.
