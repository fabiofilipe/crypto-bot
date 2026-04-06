"""
Wrapper completo para a API pública da Coinbase
Documentação: https://docs.cloud.coinbase.com/sign-in-with-coinbase/docs/api-prices
"""

import requests
from datetime import datetime
from typing import Optional
import time


class CoinbaseAPI:
    """Wrapper para API pública da Coinbase (sem necessidade de API key)"""

    BASE_URL = "https://api.coinbase.com/v2"

    def __init__(self, timeout: int = 10, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "crypto-bot/1.0",
            "Accept": "application/json",
        })

    def _request(self, endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
        """Faz requisição com retry automático"""
        url = f"{self.BASE_URL}/{endpoint}"
        for tentativa in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.Timeout:
                if tentativa < self.max_retries:
                    time.sleep(2 * tentativa)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code >= 500 and tentativa < self.max_retries:
                    time.sleep(2 * tentativa)
                else:
                    break
            except requests.exceptions.RequestException:
                if tentativa < self.max_retries:
                    time.sleep(2 * tentativa)
        return None

    # ── Preços ──────────────────────────────────────────────

    def get_spot_price(self, pair: str = "BTC-USD") -> Optional[dict]:
        """Preço spot atual de um par de moedas"""
        data = self._request(f"prices/{pair}/spot")
        return data.get("data") if data else None

    def get_buy_price(self, pair: str = "BTC-USD") -> Optional[dict]:
        """Preço de compra (inclui spread da Coinbase)"""
        data = self._request(f"prices/{pair}/buy")
        return data.get("data") if data else None

    def get_sell_price(self, pair: str = "BTC-USD") -> Optional[dict]:
        """Preço de venda (inclui spread da Coinbase)"""
        data = self._request(f"prices/{pair}/sell")
        return data.get("data") if data else None

    def get_historic_prices(self, pair: str = "BTC-USD", currency: str = "USD") -> Optional[list]:
        """Dados históricos de preços"""
        data = self._request(f"prices/{pair}/hist", params={"currency": currency})
        return data.get("data") if data else None

    # ── Exchange Rates ──────────────────────────────────────

    def get_exchange_rates(self, currency: str = "USD") -> Optional[dict]:
        """Taxas de câmbio para uma moeda base"""
        data = self._request(f"exchange-rates", params={"currency": currency})
        return data.get("data") if data else None

    def get_rate_to_currency(self, currency: str = "USD", target: str = "BRL") -> Optional[float]:
        """Obter taxa de câmbio de uma moeda para outra"""
        rates = self.get_exchange_rates(currency)
        if rates and "rates" in rates:
            rate_str = rates["rates"].get(target)
            if rate_str:
                return float(rate_str)
        return None

    # ── Currencies / Assets ─────────────────────────────────

    def get_currencies(self) -> Optional[list]:
        """Lista todas as moedas suportadas"""
        data = self._request("currencies")
        return data.get("data") if data else None

    def get_exchange_rates_for_currency(self, base: str = "USD") -> Optional[dict]:
        """Taxas de câmbio completas para uma moeda base"""
        data = self._request(f"exchange-rates", params={"currency": base})
        return data.get("data") if data else None

    def get_asset_info(self, asset_id: str) -> Optional[dict]:
        """Informações sobre um ativo específico"""
        currencies = self.get_currencies()
        if currencies:
            for c in currencies:
                if c.get("id", "").upper() == asset_id.upper():
                    return c
        return None

    # ── Market Data (simulado via API pública) ─────────────

    def get_market_data(self, pair: str = "BTC-USD") -> Optional[dict]:
        """
        Dados de mercado completos para um par.
        Combina spot, buy, sell prices em um único dict.
        """
        spot = self.get_spot_price(pair)
        buy = self.get_buy_price(pair)
        sell = self.get_sell_price(pair)

        if not spot:
            return None

        result = {
            "id": pair,
            "base": spot.get("base", pair.split("-")[0]),
            "currency": spot.get("currency", "USD"),
            "spot_price": float(spot.get("amount", 0)),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        if buy:
            result["buy_price"] = float(buy.get("amount", 0))
        if sell:
            result["sell_price"] = float(sell.get("amount", 0))

        # Calcular spread
        if "buy_price" in result and "sell_price" in result:
            result["spread"] = result["buy_price"] - result["sell_price"]
            result["spread_pct"] = (result["spread"] / result["spot_price"]) * 100

        return result

    def get_multiple_prices(self, pairs: list) -> dict:
        """Obter preços de múltiplos pares"""
        results = {}
        for pair in pairs:
            data = self.get_market_data(pair)
            if data:
                results[pair] = data
        return results
