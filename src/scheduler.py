"""
Sistema de agendamento automático para coleta de dados
Execute: python -m scheduler (com PYTHONPATH=/app/src)
"""

import schedule
import time
from datetime import datetime

from pipeline import PipelineColeta
from utils.logger import configurar_logger


class AgendadorPipeline:
    """Gerencia execução agendada do pipeline"""
    
    def __init__(self):
        self.pipeline = PipelineColeta()
        self.logger = configurar_logger('scheduler')
        self.execucoes = 0
    
    def executar_coleta(self):
        """Executa uma coleta agendada"""
        self.execucoes += 1
        
        self.logger.info("=" * 60)
        self.logger.info(f"Execução agendada #{self.execucoes} iniciada")
        self.logger.info("=" * 60)
        
        try:
            resultados = self.pipeline.executar()
            
            self.logger.info(f"Coleta #{self.execucoes} concluída com sucesso")
            self.logger.info(f"Sucessos: {len(resultados['sucesso'])} | Falhas: {len(resultados['falha'])}")
            
            return resultados
            
        except Exception as e:
            self.logger.error(f"Erro na execução agendada: {e}", exc_info=True)
            return None
    
    def agendar(self, intervalo_minutos=30):
        """Agenda execuções periódicas"""
        self.logger.info("=" * 60)
        self.logger.info("🕐 SISTEMA DE AGENDAMENTO INICIADO")
        self.logger.info("=" * 60)
        self.logger.info(f"Intervalo configurado: {intervalo_minutos} minutos")
        self.logger.info("Pressione Ctrl+C para parar")
        self.logger.info("=" * 60)
        
        # Executar imediatamente ao iniciar
        print("\n⚡ Executando primeira coleta...")
        self.executar_coleta()
        
        # Agendar execuções futuras
        schedule.every(intervalo_minutos).minutes.do(self.executar_coleta)
        
        # Loop principal
        try:
            while True:
                schedule.run_pending()
                
                # Calcular tempo até próxima execução
                proxima_exec = schedule.next_run()
                if proxima_exec:
                    tempo_restante = (proxima_exec - datetime.now()).total_seconds()
                    minutos = int(tempo_restante // 60)
                    segundos = int(tempo_restante % 60)
                    
                    print(f"\r⏰ Próxima coleta em: {minutos:02d}:{segundos:02d}   ", end='', flush=True)
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("\n\n🛑 Agendamento interrompido pelo usuário")
            self.logger.info(f"Total de execuções: {self.execucoes}")
            print("\n\n✅ Sistema encerrado com sucesso!")


def main():
    """Função principal com opções de agendamento"""
    print("\n" + "=" * 60)
    print("⏰ SISTEMA DE AGENDAMENTO AUTOMÁTICO")
    print("=" * 60)
    print("\nEscolha o intervalo de coleta:")
    print("1. A cada 5 minutos (testes)")
    print("2. A cada 15 minutos")
    print("3. A cada 30 minutos (recomendado)")
    print("4. A cada 1 hora")
    print("5. A cada 6 horas")
    print("6. Personalizado")
    print("=" * 60)
    
    opcao = input("\nEscolha uma opção (padrão: 3): ").strip()
    
    intervalos = {
        '1': 5,
        '2': 15,
        '3': 30,
        '4': 60,
        '5': 360
    }
    
    if opcao == '6':
        try:
            intervalo = int(input("Digite o intervalo em minutos: "))
        except ValueError:
            print("❌ Valor inválido, usando 30 minutos")
            intervalo = 30
    else:
        intervalo = intervalos.get(opcao, 30)
    
    print(f"\n✅ Agendamento configurado para a cada {intervalo} minutos")
    print("=" * 60)
    
    agendador = AgendadorPipeline()
    agendador.agendar(intervalo_minutos=intervalo)


if __name__ == "__main__":
    main()