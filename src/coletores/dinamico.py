from datetime import datetime
from .base import ColetorBase
from ..utils.coinbase_api import CoinbaseAPI


class ColetorDinamico(ColetorBase):
    """Coletor genérico para qualquer par de cripto via Coinbase API"""

    def __init__(self, simbolo: str, nome: str = None, par: str = "USD"):
        """
        Args:
            simbolo: Símbolo do ativo (BTC, ETH, SOL, etc.)
            nome: Nome completo (opcional, usa símbolo se None)
            par: Par de moeda (padrão: USD)
        """
        self.simbolo = simbolo.upper()
        self.par = f"{self.simbolo}-{par}"
        self.api = CoinbaseAPI()
        super().__init__(
            nome_ativo=self.simbolo,
            url_api=f"https://api.coinbase.com/v2/prices/{self.par}/spot"
        )

    def coletar(self):
        """Coleta preço spot atual"""
        dados_api = self.fazer_requisicao()

        if not dados_api:
            return None

        data_info = dados_api.get("data", {})
        preco = data_info.get("amount")

        if not preco:
            return None

        return {
            "ativo": data_info.get("base", self.simbolo),
            "preco": float(preco),
            "moeda": data_info.get("currency", "USD"),
            "horario_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
