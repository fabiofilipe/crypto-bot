"""
Dashboard simples em terminal para monitoramento
Execute: python src/dashboard.py
"""

import time
import os
from datetime import datetime
from database.db_manager import DatabaseManager
from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)


class Dashboard:
    """Dashboard de monitoramento em tempo real"""
    
    def __init__(self, intervalo_atualizacao=10):
        self.db = DatabaseManager()
        self.intervalo = intervalo_atualizacao
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def obter_dados_resumo(self):
        """Obtém resumo de todos os ativos"""
        ativos = self.db.listar_ativos()
        resumo = []
        
        for ativo_info in ativos:
            ativo = ativo_info['ativo']
            
            # Último preço
            ultimo = self.db.obter_ultimo_preco(ativo)
            
            # Estatísticas do dia
            stats_dia = self.db.obter_estatisticas(ativo, dias=1)
            
            # Estatísticas da semana
            stats_semana = self.db.obter_estatisticas(ativo, dias=7)
            
            if ultimo and stats_dia and stats_semana:
                # Calcular variações
                var_dia = 0
                if stats_dia['preco_minimo'] > 0:
                    var_dia = ((stats_dia['preco_maximo'] - stats_dia['preco_minimo']) / stats_dia['preco_minimo']) * 100
                
                var_semana = 0
                if stats_semana['preco_minimo'] > 0:
                    var_semana = ((stats_semana['preco_maximo'] - stats_semana['preco_minimo']) / stats_semana['preco_minimo']) * 100
                
                resumo.append({
                    'ativo': ativo,
                    'preco_atual': ultimo['preco'],
                    'moeda': ultimo['moeda'],
                    'horario': ultimo['horario_coleta'],
                    'coletas_dia': stats_dia['total_registros'],
                    'min_dia': stats_dia['preco_minimo'],
                    'max_dia': stats_dia['preco_maximo'],
                    'media_dia': stats_dia['preco_medio'],
                    'var_dia': var_dia,
                    'media_semana': stats_semana['preco_medio'],
                    'var_semana': var_semana
                })
        
        return resumo
    
    def formatar_variacao(self, valor):
        """Formata variação com cores"""
        if valor > 0:
            return f"{Fore.GREEN}+{valor:.2f}%{Style.RESET_ALL}"
        elif valor < 0:
            return f"{Fore.RED}{valor:.2f}%{Style.RESET_ALL}"
        else:
            return f"{valor:.2f}%"
    
    def renderizar(self):
        """Renderiza o dashboard"""
        self.limpar_tela()
        
        # Header
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'📊 DASHBOARD DE MONITORAMENTO - CRIPTOMOEDAS':^80}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"\n🕐 Atualizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔄 Próxima atualização em {self.intervalo} segundos\n")
        
        # Dados dos ativos
        dados = self.obter_dados_resumo()
        
        if not dados:
            print(f"\n{Fore.YELLOW}⚠️  Nenhum dado disponível ainda{Style.RESET_ALL}")
            return
        
        for item in dados:
            print(f"{Fore.YELLOW}{'─' * 80}{Style.RESET_ALL}")
            print(f"\n{Fore.WHITE}{Style.BRIGHT}{item['ativo']} - {item['moeda']}{Style.RESET_ALL}")
            print(f"└─ Última atualização: {item['horario']}\n")
            
            # Preço atual (destaque)
            print(f"   💰 Preço Atual:  {Fore.CYAN}{Style.BRIGHT}${item['preco_atual']:,.2f}{Style.RESET_ALL}")
            
            # Estatísticas do dia
            print(f"\n   📅 Hoje ({item['coletas_dia']} coletas):")
            print(f"      Min: ${item['min_dia']:,.2f}  |  Max: ${item['max_dia']:,.2f}  |  Média: ${item['media_dia']:,.2f}")
            print(f"      Variação: {self.formatar_variacao(item['var_dia'])}")
            
            # Estatísticas da semana
            print(f"\n   📊 Semana:")
            print(f"      Média: ${item['media_semana']:,.2f}")
            print(f"      Variação: {self.formatar_variacao(item['var_semana'])}")
            
            print()
        
        print(f"{Fore.CYAN}{'=' * 80}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}💡 Pressione Ctrl+C para sair{Style.RESET_ALL}")
    
    def executar(self):
        """Loop principal do dashboard"""
        print(f"\n{Fore.GREEN}🚀 Iniciando dashboard...{Style.RESET_ALL}")
        time.sleep(2)
        
        try:
            while True:
                self.renderizar()
                time.sleep(self.intervalo)
                
        except KeyboardInterrupt:
            self.limpar_tela()
            print(f"\n{Fore.GREEN}✅ Dashboard encerrado{Style.RESET_ALL}\n")


def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("📊 DASHBOARD DE MONITORAMENTO")
    print("=" * 80)
    print("\nEscolha o intervalo de atualização:")
    print("1. 5 segundos (atualização rápida)")
    print("2. 10 segundos (recomendado)")
    print("3. 30 segundos")
    print("4. 60 segundos")
    print("=" * 80)
    
    opcao = input("\nEscolha uma opção (padrão: 2): ").strip()
    
    intervalos = {
        '1': 5,
        '2': 10,
        '3': 30,
        '4': 60
    }
    
    intervalo = intervalos.get(opcao, 10)
    
    dashboard = Dashboard(intervalo_atualizacao=intervalo)
    dashboard.executar()


if __name__ == "__main__":
    main()