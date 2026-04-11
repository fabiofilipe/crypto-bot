# Skill: Adicionar Nova Cripto

## Descrição
Adiciona uma nova criptomoeda ao sistema de coleta de forma rápida e segura.

## Como Usar
Quando o usuário pedir "adicione [CRYPTO] ao sistema", use este skill.

## Processo
1. Leia src/pipeline.py para encontrar ATIVOS_DISPONIVEIS
2. Adicione o novo ativo à lista:
   ```python
   ATIVOS_DISPONIVEIS = [
       ...
       ("NOVO", "NomeDaCripto"),  # adicionado
   ]
   ```
3. Verifique se o ColetorDinamico suporta o novo símbolo (deve suportar automaticamente)
4. Atualize o mapa de aliases no bot_discord.py (_resolver_ativo):
   ```python
   mapa = {
       ...
       "NOME": "NOVO", "NOVO": "NOVO",
   }
   ```
5. Rode uma coleta de teste: `python -m src.pipeline` (com PYTHONPATH)
6. Verifique no banco: `SELECT * FROM precos WHERE ativo = 'NOVO' ORDER BY horario_coleta DESC LIMIT 1`

## Validação
- [ ] Ativo adicionado em ATIVOS_DISPONIVEIS
- [ ] Aliases adicionados em _resolver_ativo (bot_discord.py)
- [ ] Coleta individual funciona: ColetorDinamico("NOVO").executar()
- [ ] Registro no banco: SELECT ativo FROM ativos WHERE simbolo = 'NOVO'
- [ ] Comando Discord funciona: !crypto NOVO

## Rollback
Se algo falhar, remova a linha adicionada em ATIVOS_DISPONIVEIS e os aliases.

## Notas
- O ColetorDinamico constrói o par automaticamente: "{simbolo}-USD"
- Se a Coinbase não suportar o par, a coleta falhará com HTTP 404
- Sempre teste a coleta individual antes de adicionar ao pipeline
