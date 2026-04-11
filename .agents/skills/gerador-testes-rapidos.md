# Skill: Gerador de Testes Rápidos

## Descrição
Gera testes unitários automaticamente para qualquer módulo Python do projeto.

## Como Usar
Quando o usuário pedir "crie testes para [módulo]", use este skill.

## Processo
1. Identifique o módulo alvo (ex: src/alertas.py)
2. Leia o arquivo completo
3. Identifique todas as classes e funções públicas
4. Para cada função/classe:
   - Teste o caminho feliz (happy path)
   - Teste inputs inválidos
   - Teste edge cases (None, vazio, zero, negativo)
   - Teste exceções esperadas
5. Crie fixtures necessários (mocks de DB, API, etc.)
6. Salve em tests/test_[nome].py

## Template de Teste
```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.[modulo] import [ClasseOuFuncao]

class Test[Classe]:
    """Testes para [Classe]"""
    
    def test_cenario_feliz(self):
        """Testa o comportamento esperado"""
        # Arrange
        obj = [Classe]()
        
        # Act
        resultado = obj.metodo()
        
        # Assert
        assert resultado == esperado
    
    def test_edge_case(self):
        """Testa limite ou condição especial"""
        pass
    
    @pytest.mark.parametrize("input_invalido", [None, "", 0, -1])
    def test_input_invalido(self, input_invalido):
        """Valida tratamento de erro"""
        with pytest.raises((ValueError, TypeError)):
            obj.metodo(input_invalido)
```

## Fixtures Comuns para Este Projeto
```python
# conftest.py
@pytest.fixture
def mock_db():
    """Mock do DatabaseManager"""
    with patch("src.database.db_manager.DatabaseManager") as mock:
        mock.return_value.obter_ultimo_preco.return_value = {
            "ativo": "BTC",
            "preco": 50000.00,
            "moeda": "USD",
            "horario_coleta": "2024-01-01 12:00:00"
        }
        yield mock

@pytest.fixture
def mock_coinbase_api():
    """Mock do CoinbaseAPI"""
    with patch("src.utils.coinbase_api.CoinbaseAPI") as mock:
        mock.return_value.get_spot_price.return_value = {"data": {"amount": "50000.00"}}
        yield mock

@pytest.fixture
def sample_price_data():
    """Dados de exemplo para testes"""
    return {
        "ativo": "BTC",
        "preco": 50000.00,
        "moeda": "USD",
        "horario_coleta": "2024-01-01 12:00:00"
    }
```

## Output
- Arquivo tests/test_[modulo].py criado
- Conftest.py atualizado com fixtures necessárias
- Instruções para rodar: `pytest tests/test_[modulo].py -v`
