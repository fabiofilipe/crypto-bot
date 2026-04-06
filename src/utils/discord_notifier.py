"""
Módulo para enviar notificações para Discord via webhook
"""

import requests
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class DiscordNotifier:
    """Gerencia envio de notificações para Discord"""

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Inicializa o notificador Discord

        Args:
            webhook_url: URL do webhook do Discord (opcional, pode vir do .env)
        """
        self.webhook_url = webhook_url or os.getenv('DISCORD_WEBHOOK_URL')

        if not self.webhook_url:
            raise ValueError(
                "DISCORD_WEBHOOK_URL não configurada. "
                "Configure no arquivo .env ou passe como parâmetro."
            )

    def enviar_alerta_variacao(self, alerta: dict) -> bool:
        """
        Envia alerta de variação de preço para Discord

        Args:
            alerta: Dicionário com dados do alerta

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Definir cor baseado no tipo de variação
            cor = 0x00ff00 if alerta['tipo'] == 'ALTA' else 0xff0000  # Verde ou Vermelho
            emoji = "📈" if alerta['tipo'] == 'ALTA' else "📉"

            # Criar embed rico para Discord
            embed = {
                "title": f"{emoji} Alerta de Variação - {alerta['ativo']}",
                "color": cor,
                "fields": [
                    {
                        "name": "📊 Variação",
                        "value": f"**{alerta['variacao']:+.2f}%**",
                        "inline": True
                    },
                    {
                        "name": "💰 Preço Anterior",
                        "value": f"${alerta['preco_anterior']:,.2f}",
                        "inline": True
                    },
                    {
                        "name": "💵 Preço Atual",
                        "value": f"${alerta['preco_atual']:,.2f}",
                        "inline": True
                    }
                ],
                "timestamp": datetime.now().isoformat(),
                "footer": {
                    "text": "Sistema de Coleta Financeira"
                }
            }

            payload = {
                "embeds": [embed]
            }

            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            return True

        except Exception as e:
            print(f"Erro ao enviar alerta para Discord: {e}")
            return False

    def enviar_alerta_limite(self, alerta: dict) -> bool:
        """
        Envia alerta de limite de preço para Discord

        Args:
            alerta: Dicionário com dados do alerta

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Definir cor baseado no tipo
            cor = 0xff0000 if alerta['tipo'] == 'ABAIXO_MINIMO' else 0xffa500  # Vermelho ou Laranja
            emoji = "⚠️"

            tipo_msg = "Abaixo do Mínimo" if alerta['tipo'] == 'ABAIXO_MINIMO' else "Acima do Máximo"

            embed = {
                "title": f"{emoji} Alerta de Limite - {alerta['ativo']}",
                "description": f"**{tipo_msg}**",
                "color": cor,
                "fields": [
                    {
                        "name": "💵 Preço Atual",
                        "value": f"${alerta['preco_atual']:,.2f}",
                        "inline": True
                    },
                    {
                        "name": "🎯 Limite Definido",
                        "value": f"${alerta['limite']:,.2f}",
                        "inline": True
                    }
                ],
                "timestamp": datetime.now().isoformat(),
                "footer": {
                    "text": "Sistema de Coleta Financeira"
                }
            }

            payload = {
                "embeds": [embed]
            }

            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            return True

        except Exception as e:
            print(f"Erro ao enviar alerta de limite para Discord: {e}")
            return False

    def enviar_mensagem_simples(self, mensagem: str, urgente: bool = False) -> bool:
        """
        Envia mensagem simples para Discord

        Args:
            mensagem: Texto da mensagem
            urgente: Se True, menciona @everyone

        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            content = mensagem
            if urgente:
                content = f"@everyone {mensagem}"

            payload = {
                "content": content
            }

            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            return True

        except Exception as e:
            print(f"Erro ao enviar mensagem para Discord: {e}")
            return False

    def testar_conexao(self) -> bool:
        """
        Testa a conexão com o webhook do Discord

        Returns:
            True se conectado com sucesso, False caso contrário
        """
        try:
            payload = {
                "content": "✅ Teste de conexão - Sistema de Coleta Financeira funcionando!"
            }

            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()

            print("✅ Conexão com Discord estabelecida com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro ao testar conexão com Discord: {e}")
            return False


def exemplo_uso():
    """Exemplo de uso do notificador Discord"""
    try:
        notifier = DiscordNotifier()

        # Testar conexão
        notifier.testar_conexao()

        # Exemplo de alerta de variação
        alerta_variacao = {
            'ativo': 'BTC',
            'preco_anterior': 67000.00,
            'preco_atual': 70350.00,
            'variacao': 5.0,
            'tipo': 'ALTA',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        notifier.enviar_alerta_variacao(alerta_variacao)

        # Exemplo de alerta de limite
        alerta_limite = {
            'ativo': 'BTC',
            'preco_atual': 48000.00,
            'limite': 50000.00,
            'tipo': 'ABAIXO_MINIMO',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        notifier.enviar_alerta_limite(alerta_limite)

    except ValueError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    exemplo_uso()
