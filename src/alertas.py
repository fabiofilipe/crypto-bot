"""
Sistema de alertas para variações de preço
"""

from database.db_manager import DatabaseManager
from utils.logger import configurar_logger
from utils.discord_notifier import DiscordNotifier
from datetime import datetime
from colorama import Fore, Style, init
import os

# Inicializar colorama para cores no terminal
init(autoreset=True)


class SistemaAlertas:
    """Gerencia alertas de variação de preços"""

    def __init__(self, discord_habilitado=True):
        self.db = DatabaseManager()
        self.logger = configurar_logger('alertas')
        self.historico_alertas = []

        # Tentar inicializar Discord notifier
        self.discord_notifier = None
        if discord_habilitado:
            try:
                # Verifica se a URL do webhook está configurada
                webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
                if webhook_url:
                    self.discord_notifier = DiscordNotifier()
                    self.logger.info("Discord notifier habilitado")
                else:
                    self.logger.info("Discord notifier não configurado (DISCORD_WEBHOOK_URL não encontrada)")
            except Exception as e:
                self.logger.warning(f"Não foi possível inicializar Discord notifier: {e}")
                self.discord_notifier = None
    
    def verificar_variacao_percentual(self, ativo, limite_percentual=5.0):
        """Verifica se houve variação significativa no preço"""
        historico = self.db.obter_historico(ativo, limite=2)
        
        if len(historico) < 2:
            return None
        
        preco_atual = historico[0]['preco']
        preco_anterior = historico[1]['preco']
        
        variacao = ((preco_atual - preco_anterior) / preco_anterior) * 100
        
        if abs(variacao) >= limite_percentual:
            alerta = {
                'ativo': ativo,
                'preco_anterior': preco_anterior,
                'preco_atual': preco_atual,
                'variacao': variacao,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'tipo': 'ALTA' if variacao > 0 else 'BAIXA'
            }
            
            self.historico_alertas.append(alerta)
            self._notificar_alerta(alerta)
            
            return alerta
        
        return None
    
    def verificar_limite_preco(self, ativo, preco_minimo=None, preco_maximo=None):
        """Verifica se o preço ultrapassou limites definidos"""
        ultimo = self.db.obter_ultimo_preco(ativo)
        
        if not ultimo:
            return None
        
        preco_atual = ultimo['preco']
        alertas = []
        
        if preco_minimo and preco_atual < preco_minimo:
            alerta = {
                'ativo': ativo,
                'preco_atual': preco_atual,
                'limite': preco_minimo,
                'tipo': 'ABAIXO_MINIMO',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            alertas.append(alerta)
            self._notificar_limite(alerta)
        
        if preco_maximo and preco_atual > preco_maximo:
            alerta = {
                'ativo': ativo,
                'preco_atual': preco_atual,
                'limite': preco_maximo,
                'tipo': 'ACIMA_MAXIMO',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            alertas.append(alerta)
            self._notificar_limite(alerta)
        
        return alertas if alertas else None
    
    def verificar_todos_ativos(self, limite_percentual=5.0):
        """Verifica variações em todos os ativos"""
        ativos = self.db.listar_ativos()
        alertas_gerados = []
        
        for ativo_info in ativos:
            ativo = ativo_info['ativo']
            alerta = self.verificar_variacao_percentual(ativo, limite_percentual)
            
            if alerta:
                alertas_gerados.append(alerta)
        
        return alertas_gerados
    
    def _notificar_alerta(self, alerta):
        """Notifica variação de preço (terminal + log + Discord)"""
        cor = Fore.GREEN if alerta['tipo'] == 'ALTA' else Fore.RED
        emoji = "📈" if alerta['tipo'] == 'ALTA' else "📉"

        mensagem = f"""
{cor}{'=' * 60}
{emoji} ALERTA DE VARIAÇÃO - {alerta['ativo']}
{'=' * 60}{Style.RESET_ALL}
Variação: {cor}{alerta['variacao']:+.2f}%{Style.RESET_ALL}
Preço anterior: ${alerta['preco_anterior']:,.2f}
Preço atual: ${alerta['preco_atual']:,.2f}
Horário: {alerta['timestamp']}
{cor}{'=' * 60}{Style.RESET_ALL}
"""
        print(mensagem)

        self.logger.warning(
            f"ALERTA {alerta['ativo']}: Variação de {alerta['variacao']:+.2f}% "
            f"(${alerta['preco_anterior']:,.2f} → ${alerta['preco_atual']:,.2f})"
        )

        # Enviar para Discord se habilitado
        if self.discord_notifier:
            try:
                self.discord_notifier.enviar_alerta_variacao(alerta)
            except Exception as e:
                self.logger.error(f"Erro ao enviar alerta para Discord: {e}")
    
    def _notificar_limite(self, alerta):
        """Notifica ultrapassagem de limite (terminal + log + Discord)"""
        cor = Fore.RED if alerta['tipo'] == 'ABAIXO_MINIMO' else Fore.YELLOW
        emoji = "⚠️"

        tipo_msg = "ABAIXO DO MÍNIMO" if alerta['tipo'] == 'ABAIXO_MINIMO' else "ACIMA DO MÁXIMO"

        mensagem = f"""
{cor}{'=' * 60}
{emoji} ALERTA DE LIMITE - {alerta['ativo']}
{'=' * 60}{Style.RESET_ALL}
Tipo: {tipo_msg}
Preço atual: ${alerta['preco_atual']:,.2f}
Limite: ${alerta['limite']:,.2f}
Horário: {alerta['timestamp']}
{cor}{'=' * 60}{Style.RESET_ALL}
"""
        print(mensagem)

        self.logger.warning(
            f"ALERTA {alerta['ativo']}: Preço ${alerta['preco_atual']:,.2f} "
            f"{tipo_msg.lower()} (limite: ${alerta['limite']:,.2f})"
        )

        # Enviar para Discord se habilitado
        if self.discord_notifier:
            try:
                self.discord_notifier.enviar_alerta_limite(alerta)
            except Exception as e:
                self.logger.error(f"Erro ao enviar alerta de limite para Discord: {e}")
    
    def obter_historico_alertas(self, limite=10):
        """Retorna histórico de alertas gerados"""
        return self.historico_alertas[-limite:]
    
    def limpar_historico(self):
        """Limpa histórico de alertas"""
        self.historico_alertas.clear()
        self.logger.info("Histórico de alertas limpo")


def exemplo_uso():
    """Exemplo de uso do sistema de alertas"""
    alertas = SistemaAlertas()
    
    print("\n" + "=" * 60)
    print("🔔 VERIFICANDO ALERTAS")
    print("=" * 60)
    
    # Verificar variações em todos os ativos
    alertas_gerados = alertas.verificar_todos_ativos(limite_percentual=3.0)
    
    if not alertas_gerados:
        print("\n✅ Nenhuma variação significativa detectada")
    
    # Exemplo de limite de preço
    print("\n" + "=" * 60)
    print("📊 VERIFICANDO LIMITES")
    print("=" * 60)
    
    # Verificar se Bitcoin está fora dos limites (exemplo)
    alertas.verificar_limite_preco('BTC', preco_minimo=50000, preco_maximo=70000)
    
    print("\n✅ Verificação concluída!")


if __name__ == "__main__":
    exemplo_uso()