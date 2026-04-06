from .dinamico import ColetorDinamico


class ColetorBitcoin(ColetorDinamico):
    """Coletor de Bitcoin"""

    def __init__(self):
        super().__init__(simbolo="BTC", nome="Bitcoin")
