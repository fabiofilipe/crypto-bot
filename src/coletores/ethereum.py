from .dinamico import ColetorDinamico


class ColetorEthereum(ColetorDinamico):
    """Coletor de Ethereum"""

    def __init__(self):
        super().__init__(simbolo="ETH", nome="Ethereum")
