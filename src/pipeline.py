"""
Pipeline de coleta de criptomoedas - dinâmico e expansível
"""

from datetime import datetime
from utils.logger import configurar_logger
from coletores.bitcoin import ColetorBitcoin
from coletores.ethereum import ColetorEthereum
from coletores.dinamico import ColetorDinamico
from database.db_manager import DatabaseManager

try:
    from alertas import SistemaAlertas
    ALERTAS_DISPONIVEL = True
except ImportError:
    ALERTAS_DISPONIVEL = False


# Registro de ativos disponíveis
ATIVOS_DISPONIVEIS = [
    ("BTC", "Bitcoin"),
    ("ETH", "Ethereum"),
    ("SOL", "Solana"),
    ("DOGE", "Dogecoin"),
    ("XRP", "Ripple"),
    ("ADA", "Cardano"),
    ("AVAX", "Avalanche"),
    ("DOT", "Polkadot"),
    ("LINK", "Chainlink"),
    ("MATIC", "Polygon"),
    ("LTC", "Litecoin"),
    ("SHIB", "Shiba Inu"),
]


def obter_coletor(simbolo: str):
    """Fabrica de coletores por símbolo"""
    simbolo = simbolo.upper()
    mapa = {
        "BTC": ColetorBitcoin,
        "ETH": ColetorEthereum,
    }
    cls = mapa.get(simbolo)
    if cls:
        return cls()
    nome = dict(ATIVOS_DISPONIVEIS).get(simbolo)
    return ColetorDinamico(simbolo=simbolo, nome=nome)


def todos_coletores():
    """Retorna instâncias de todos os coletores ativos"""
    return [obter_coletor(s) for s, _ in ATIVOS_DISPONIVEIS]


class PipelineColeta:
    """Pipeline principal para orquestrar a coleta de dados"""

    def __init__(self, habilitar_alertas=True, limite_variacao=3.0, ativos: list = None):
        if ativos:
            self.coletores = [obter_coletor(s) for s in ativos]
        else:
            # CORRIGIDO: coleta TODOS os ativos por default, não apenas BTC+ETH
            self.coletores = todos_coletores()

        self.db = DatabaseManager()
        self.logger = configurar_logger("pipeline")

        # Registrar ativos no DB
        for simbolo, nome in ATIVOS_DISPONIVEIS:
            self.db.registrar_ativo(simbolo, nome, f"{simbolo}-USD")

        # Alertas
        self.sistema_alertas = None
        self.limite_variacao = limite_variacao
        if ALERTAS_DISPONIVEL and habilitar_alertas:
            try:
                self.sistema_alertas = SistemaAlertas()
                self.logger.info("Sistema de alertas habilitado")
            except Exception as e:
                self.logger.warning(f"Não foi possível habilitar alertas: {e}")

    def executar(self):
        """Executa todos os coletores"""
        inicio = datetime.now()

        print("=" * 60)
        print(f"🚀 Pipeline - {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        self.logger.info("=" * 60)
        self.logger.info("Pipeline iniciado")
        self.logger.info("=" * 60)

        resultados = {"sucesso": [], "falha": [], "total": len(self.coletores)}

        for coletor in self.coletores:
            nome = coletor.nome_ativo
            if coletor.executar():
                resultados["sucesso"].append(nome)
                print(f"✅ {nome} coletado com sucesso")
            else:
                resultados["falha"].append(nome)
                print(f"❌ {nome} falhou na coleta")

        # Invalidar cache após coleta (dados novos disponíveis)
        self.db.invalidate_cache()

        # Alertas
        alertas_gerados = []
        if self.sistema_alertas and resultados["sucesso"]:
            print("\n" + "=" * 60)
            print("🔔 Verificando alertas...")
            print("=" * 60)
            try:
                alertas_gerados = self.sistema_alertas.verificar_todos_ativos(
                    limite_percentual=self.limite_variacao
                )
                if alertas_gerados:
                    print(f"\n⚠️  {len(alertas_gerados)} alerta(s) detectado(s)!")
                    for a in alertas_gerados:
                        print(f"   • {a['ativo']}: {a['variacao']:+.2f}%")
                else:
                    print("\n✅ Nenhuma variação significativa detectada")
            except Exception as e:
                self.logger.error(f"Erro ao verificar alertas: {e}")

        fim = datetime.now()
        tempo = (fim - inicio).total_seconds()

        print("\n" + "=" * 60)
        print(f"📊 Relatório:")
        print(f"   ✅ Sucesso: {len(resultados['sucesso'])}")
        print(f"   ❌ Falhas: {len(resultados['falha'])}")
        if alertas_gerados:
            print(f"   🔔 Alertas: {len(alertas_gerados)}")
        print(f"   ⏱️  Tempo: {tempo:.2f}s")
        print("=" * 60)

        self.logger.info(f"Pipeline finalizado em {tempo:.2f}s")
        self.logger.info(f"Sucesso: {len(resultados['sucesso'])} | Falhas: {len(resultados['falha'])}")

        return resultados


if __name__ == "__main__":
    pipeline = PipelineColeta()
    pipeline.executar()
