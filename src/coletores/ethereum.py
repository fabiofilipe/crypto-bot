from datetime import datetime
from .base import ColetorBase


class ColetorEthereum(ColetorBase):
    """Coletor específico para Ethereum usando API Coinbase"""
    
    def __init__(self):
        super().__init__(
            nome_ativo='Ethereum',
            url_api='https://api.coinbase.com/v2/prices/ETH-USD/spot'
        )
    
    def coletar(self):
        """Coleta dados do Ethereum"""
        dados_api = self.fazer_requisicao()
        
        if not dados_api:
            return None
        
        # Extrai informações da resposta
        data_info = dados_api.get('data', {})
        
        return {
            'ativo': data_info.get('base', 'ETH'),
            'preco': float(data_info.get('amount', 0)),
            'moeda': data_info.get('currency', 'USD'),
            'horario_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }