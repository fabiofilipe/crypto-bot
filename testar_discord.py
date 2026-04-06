#!/usr/bin/env python3
"""
Script para testar a integração com Discord
"""

import sys
import os

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.discord_notifier import DiscordNotifier
from datetime import datetime


def testar_conexao():
    """Testa a conexão com o Discord"""
    print("\n" + "=" * 60)
    print("🔔 TESTANDO CONEXÃO COM DISCORD")
    print("=" * 60)

    try:
        notifier = DiscordNotifier()
        notifier.testar_conexao()
        return notifier
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
        print("\nPor favor, configure o DISCORD_WEBHOOK_URL no arquivo .env")
        return None


def testar_alerta_variacao(notifier):
    """Testa envio de alerta de variação"""
    print("\n" + "=" * 60)
    print("📈 TESTANDO ALERTA DE VARIAÇÃO (ALTA)")
    print("=" * 60)

    alerta_alta = {
        'ativo': 'BTC',
        'preco_anterior': 67000.00,
        'preco_atual': 70350.00,
        'variacao': 5.0,
        'tipo': 'ALTA',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if notifier.enviar_alerta_variacao(alerta_alta):
        print("✅ Alerta de alta enviado com sucesso!")
    else:
        print("❌ Falha ao enviar alerta de alta")

    print("\n" + "=" * 60)
    print("📉 TESTANDO ALERTA DE VARIAÇÃO (BAIXA)")
    print("=" * 60)

    alerta_baixa = {
        'ativo': 'ETH',
        'preco_anterior': 3500.00,
        'preco_atual': 3325.00,
        'variacao': -5.0,
        'tipo': 'BAIXA',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if notifier.enviar_alerta_variacao(alerta_baixa):
        print("✅ Alerta de baixa enviado com sucesso!")
    else:
        print("❌ Falha ao enviar alerta de baixa")


def testar_alerta_limite(notifier):
    """Testa envio de alerta de limite"""
    print("\n" + "=" * 60)
    print("⚠️  TESTANDO ALERTA DE LIMITE (ABAIXO DO MÍNIMO)")
    print("=" * 60)

    alerta_minimo = {
        'ativo': 'BTC',
        'preco_atual': 48000.00,
        'limite': 50000.00,
        'tipo': 'ABAIXO_MINIMO',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if notifier.enviar_alerta_limite(alerta_minimo):
        print("✅ Alerta de mínimo enviado com sucesso!")
    else:
        print("❌ Falha ao enviar alerta de mínimo")

    print("\n" + "=" * 60)
    print("⚠️  TESTANDO ALERTA DE LIMITE (ACIMA DO MÁXIMO)")
    print("=" * 60)

    alerta_maximo = {
        'ativo': 'ETH',
        'preco_atual': 5500.00,
        'limite': 5000.00,
        'tipo': 'ACIMA_MAXIMO',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    if notifier.enviar_alerta_limite(alerta_maximo):
        print("✅ Alerta de máximo enviado com sucesso!")
    else:
        print("❌ Falha ao enviar alerta de máximo")


def testar_mensagem_simples(notifier):
    """Testa envio de mensagem simples"""
    print("\n" + "=" * 60)
    print("💬 TESTANDO MENSAGEM SIMPLES")
    print("=" * 60)

    if notifier.enviar_mensagem_simples("🚀 Sistema de alertas Discord está funcionando perfeitamente!"):
        print("✅ Mensagem simples enviada com sucesso!")
    else:
        print("❌ Falha ao enviar mensagem simples")


def main():
    """Função principal"""
    notifier = testar_conexao()

    if not notifier:
        return

    print("\nAguarde enquanto enviamos os testes para o Discord...")
    print("Você deve receber 6 mensagens no canal configurado.\n")

    # Testar diferentes tipos de alertas
    testar_alerta_variacao(notifier)
    testar_alerta_limite(notifier)
    testar_mensagem_simples(notifier)

    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    print("\nVerifique seu canal no Discord para ver as notificações.")


if __name__ == "__main__":
    main()
