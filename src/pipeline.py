from datetime import datetime
from coletores.bitcoin import ColetorBitcoin
from coletores.ethereum import ColetorEthereum
from utils.logger import configurar_logger

try:
    from alertas import SistemaAlertas
    ALERTAS_DISPONIVEL = True
except ImportError:
    ALERTAS_DISPONIVEL = False


class PipelineColeta:
    """Pipeline principal para orquestrar a coleta de dados"""

    def __init__(self, habilitar_alertas=True, limite_variacao=3.0):
        self.coletores = [
            ColetorBitcoin(),
            ColetorEthereum(),
        ]
        self.logger = configurar_logger('pipeline')

        # Configurar sistema de alertas
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
        print(f"🚀 Iniciando Pipeline - {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.logger.info("=" * 60)
        self.logger.info("Pipeline iniciado")
        self.logger.info("=" * 60)
        
        resultados = {
            'sucesso': [],
            'falha': [],
            'total': len(self.coletores)
        }
        
        for coletor in self.coletores:
            nome = coletor.nome_ativo
            
            if coletor.executar():
                resultados['sucesso'].append(nome)
                print(f"✅ {nome} coletado com sucesso")
            else:
                resultados['falha'].append(nome)
                print(f"❌ {nome} falhou na coleta")
        
        # Verificar alertas se habilitado
        alertas_gerados = []
        if self.sistema_alertas and resultados['sucesso']:
            print("\n" + "=" * 60)
            print("🔔 Verificando alertas...")
            print("=" * 60)

            try:
                alertas_gerados = self.sistema_alertas.verificar_todos_ativos(
                    limite_percentual=self.limite_variacao
                )

                if alertas_gerados:
                    print(f"\n⚠️  {len(alertas_gerados)} alerta(s) detectado(s)!")
                    for alerta in alertas_gerados:
                        print(f"   • {alerta['ativo']}: {alerta['variacao']:+.2f}%")
                else:
                    print("\n✅ Nenhuma variação significativa detectada")

            except Exception as e:
                self.logger.error(f"Erro ao verificar alertas: {e}")
                print(f"\n❌ Erro ao verificar alertas: {e}")

        # Calcular tempo de execução
        fim = datetime.now()
        tempo_execucao = (fim - inicio).total_seconds()

        # Relatório final
        print("\n" + "=" * 60)
        print(f"📊 Relatório Final:")
        print(f"   ✅ Sucesso: {len(resultados['sucesso'])}")
        print(f"   ❌ Falhas: {len(resultados['falha'])}")
        if alertas_gerados:
            print(f"   🔔 Alertas: {len(alertas_gerados)}")
        print(f"   ⏱️  Tempo de execução: {tempo_execucao:.2f}s")
        print("=" * 60)
        
        # Log do relatório
        self.logger.info("=" * 60)
        self.logger.info(f"Pipeline finalizado em {tempo_execucao:.2f}s")
        self.logger.info(f"Sucesso: {len(resultados['sucesso'])} | Falhas: {len(resultados['falha'])}")
        
        if resultados['sucesso']:
            self.logger.info(f"Coletados com sucesso: {', '.join(resultados['sucesso'])}")
        
        if resultados['falha']:
            self.logger.warning(f"Falharam: {', '.join(resultados['falha'])}")
        
        self.logger.info("=" * 60)
        
        return resultados


if __name__ == "__main__":
    pipeline = PipelineColeta()
    pipeline.executar()