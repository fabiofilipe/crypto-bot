from datetime import datetime
from .base import ColetorBase


class ColetorBitcoin(ColetorBase):
    """Coletor específico para Bitcoin usando API Coinbase"""
    
    def __init__(self):
        super().__init__(
            nome_ativo='Bitcoin',
            url_api='https://api.coinbase.com/v2/prices/BTC-USD/spot'
        )
    
    def coletar(self):
        """Coleta dados do Bitcoin"""
        dados_api = self.fazer_requisicao()
        
        if not dados_api:
            return None
        
        # Extrai informações da resposta
        data_info = dados_api.get('data', {})
        
        return {
            'ativo': data_info.get('base', 'BTC'),
            'preco': float(data_info.get('amount', 0)),
            'moeda': data_info.get('currency', 'USD'),
            'horario_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }