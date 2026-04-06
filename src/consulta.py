"""
Script para consultas e análises dos dados coletados
Execute: python src/consultas.py
"""

from database.db_manager import DatabaseManager
from datetime import datetime
import pandas as pd


class ConsultasDados:
    """Classe para facilitar consultas e análises"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def listar_ativos_disponiveis(self):
        """Lista todos os ativos disponíveis no banco"""
        print("\n" + "=" * 60)
        print("📊 ATIVOS DISPONÍVEIS")
        print("=" * 60)
        
        ativos = self.db.listar_ativos()
        
        if not ativos:
            print("❌ Nenhum ativo encontrado no banco de dados")
            return
        
        for ativo in ativos:
            print(f"   • {ativo['ativo']:10s} - {ativo['total_registros']} registros")
        
        print("=" * 60)
    
    def mostrar_ultimo_preco(self, ativo):
        """Mostra o último preço de um ativo"""
        print(f"\n💰 Último Preço - {ativo}")
        print("-" * 60)
        
        dados = self.db.obter_ultimo_preco(ativo)
        
        if not dados:
            print(f"❌ Nenhum registro encontrado para {ativo}")
            return
        
        print(f"   Preço: {dados['preco']:.2f} {dados['moeda']}")
        print(f"   Data: {dados['horario_coleta']}")
        print("-" * 60)
    
    def mostrar_estatisticas(self, ativo, dias=7):
        """Mostra estatísticas de um ativo"""
        print(f"\n📈 Estatísticas - {ativo} (últimos {dias} dias)")
        print("-" * 60)
        
        stats = self.db.obter_estatisticas(ativo, dias)
        
        if not stats or stats['total_registros'] == 0:
            print(f"❌ Sem dados para {ativo} nos últimos {dias} dias")
            return
        
        print(f"   Total de registros: {stats['total_registros']}")
        print(f"   Preço Mínimo:  {stats['preco_minimo']:,.2f}")
        print(f"   Preço Médio:   {stats['preco_medio']:,.2f}")
        print(f"   Preço Máximo:  {stats['preco_maximo']:,.2f}")
        
        variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100
        print(f"   Variação:      {variacao:.2f}%")
        
        print(f"   Primeira coleta: {stats['primeira_coleta']}")
        print(f"   Última coleta:   {stats['ultima_coleta']}")
        print("-" * 60)
    
    def mostrar_historico(self, ativo, limite=10):
        """Mostra histórico recente de um ativo"""
        print(f"\n📜 Histórico Recente - {ativo} (últimos {limite} registros)")
        print("-" * 60)
        
        historico = self.db.obter_historico(ativo, limite)
        
        if not historico:
            print(f"❌ Nenhum histórico encontrado para {ativo}")
            return
        
        for registro in historico:
            print(f"   {registro['horario_coleta']} | {registro['preco']:,.2f} {registro['moeda']}")
        
        print("-" * 60)
    
    def exportar_para_csv(self, ativo, limite=1000):
        """Exporta dados de um ativo para CSV"""
        print(f"\n💾 Exportando {ativo} para CSV...")
        
        historico = self.db.obter_historico(ativo, limite)
        
        if not historico:
            print(f"❌ Nenhum dado para exportar")
            return
        
        df = pd.DataFrame(historico)
        filename = f'data/exportacao_{ativo.lower()}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        df.to_csv(filename, index=False)
        
        print(f"✅ Exportado: {filename} ({len(historico)} registros)")
    
    def comparar_ativos(self, ativos, dias=7):
        """Compara múltiplos ativos"""
        print(f"\n📊 Comparação de Ativos (últimos {dias} dias)")
        print("=" * 60)
        
        for ativo in ativos:
            stats = self.db.obter_estatisticas(ativo, dias)
            
            if stats and stats['total_registros'] > 0:
                variacao = ((stats['preco_maximo'] - stats['preco_minimo']) / stats['preco_minimo']) * 100
                print(f"\n{ativo}:")
                print(f"   Média: {stats['preco_medio']:,.2f} | Variação: {variacao:.2f}%")
        
        print("=" * 60)


def menu_interativo():
    """Menu interativo para consultas"""
    consultas = ConsultasDados()
    
    while True:
        print("\n" + "=" * 60)
        print("🔍 SISTEMA DE CONSULTAS - CRIPTOMOEDAS")
        print("=" * 60)
        print("1. Listar ativos disponíveis")
        print("2. Ver último preço")
        print("3. Ver estatísticas")
        print("4. Ver histórico")
        print("5. Comparar ativos")
        print("6. Exportar para CSV")
        print("0. Sair")
        print("=" * 60)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '0':
            print("\n👋 Até logo!")
            break
        
        elif opcao == '1':
            consultas.listar_ativos_disponiveis()
        
        elif opcao == '2':
            ativo = input("Digite o ativo (ex: BTC): ").strip().upper()
            consultas.mostrar_ultimo_preco(ativo)
        
        elif opcao == '3':
            ativo = input("Digite o ativo (ex: BTC): ").strip().upper()
            dias = input("Dias para análise (padrão: 7): ").strip()
            dias = int(dias) if dias.isdigit() else 7
            consultas.mostrar_estatisticas(ativo, dias)
        
        elif opcao == '4':
            ativo = input("Digite o ativo (ex: BTC): ").strip().upper()
            limite = input("Quantidade de registros (padrão: 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            consultas.mostrar_historico(ativo, limite)
        
        elif opcao == '5':
            ativos_str = input("Digite os ativos separados por vírgula (ex: BTC,ETH): ").strip()
            ativos = [a.strip().upper() for a in ativos_str.split(',')]
            dias = input("Dias para análise (padrão: 7): ").strip()
            dias = int(dias) if dias.isdigit() else 7
            consultas.comparar_ativos(ativos, dias)
        
        elif opcao == '6':
            ativo = input("Digite o ativo (ex: BTC): ").strip().upper()
            limite = input("Quantidade de registros (padrão: 1000): ").strip()
            limite = int(limite) if limite.isdigit() else 1000
            consultas.exportar_para_csv(ativo, limite)
        
        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    menu_interativo()