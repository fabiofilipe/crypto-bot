---
name: gerador-testes
description: Gera testes unitários automaticamente para qualquer módulo Python do projeto. Use para "crie testes para [módulo]".
---

## Processo
1. Leia o módulo alvo (ex: src/alertas.py)
2. Identifique todas as classes e funções públicas
3. Para cada função/classe: happy path + inputs inválidos + edge cases + exceções
4. Crie fixtures necessários (mocks de DB, API, etc.)
5. Salve em tests/test_[nome].py

## Fixtures Comuns
```python
@pytest.fixture
def mock_db():
    with patch("src.database.db_manager.DatabaseManager") as mock:
        mock.return_value.obter_ultimo_preco.return_value = {
            "ativo": "BTC", "preco": 50000.00, "moeda": "USD",
            "horario_coleta": "2024-01-01 12:00:00"
        }
        yield mock

@pytest.fixture
def mock_coinbase_api():
    with patch("src.utils.coinbase_api.CoinbaseAPI") as mock:
        mock.return_value.get_spot_price.return_value = {"data": {"amount": "50000.00"}}
        yield mock
```

## Regras
- One assertion per test idealmente
- Nomes descritivos: `test_coletor_retry_on_timeout`
- Mock dependencies externos
- Teste happy path E error cases
- Tests passam independentemente
- Alvo: 80%+ coverage
