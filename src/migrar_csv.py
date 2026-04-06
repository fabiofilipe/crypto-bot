"""
Script para migrar dados dos CSVs existentes para o SQLite
Execute: python src/migrar_csv.py
"""

import pandas as pd
from pathlib import Path
from database.db_manager import DatabaseManager


def migrar_csv_para_sqlite():
    """Migra todos os CSVs de data/raw para o SQLite"""
    
    print("\n" + "=" * 60)
    print("🔄 MIGRAÇÃO DE DADOS: CSV → SQLite")
    print("=" * 60)
    
    db = DatabaseManager()
    data_dir = Path('data/raw')
    
    if not data_dir.exists():
        print("❌ Diretório data/raw não encontrado")
        return
    
    # Buscar todos os CSVs
    arquivos_csv = list(data_dir.glob('preco_*.csv'))
    
    if not arquivos_csv:
        print("❌ Nenhum arquivo CSV encontrado em data/raw/")
        return
    
    print(f"\n📁 Encontrados {len(arquivos_csv)} arquivo(s) CSV\n")
    
    total_migrados = 0
    total_erros = 0
    
    for arquivo in arquivos_csv:
        print(f"🔄 Processando: {arquivo.name}")
        
        try:
            # Ler CSV
            df = pd.read_csv(arquivo)
            
            # Validar colunas necessárias
            colunas_necessarias = ['ativo', 'preco', 'moeda', 'horario_coleta']
            if not all(col in df.columns for col in colunas_necessarias):
                print(f"   ⚠️  Colunas incorretas, pulando...")
                continue
            
            # Inserir cada registro
            registros_arquivo = 0
            for _, row in df.iterrows():
                try:
                    id_inserido = db.inserir_preco(
                        ativo=row['ativo'],
                        preco=float(row['preco']),
                        moeda=row['moeda'],
                        horario_coleta=row['horario_coleta']
                    )
                    
                    if id_inserido:
                        registros_arquivo += 1
                    else:
                        total_erros += 1
                        
                except Exception as e:
                    print(f"   ❌ Erro no registro: {e}")
                    total_erros += 1
            
            total_migrados += registros_arquivo
            print(f"   ✅ {registros_arquivo} registros migrados")
            
        except Exception as e:
            print(f"   ❌ Erro ao processar arquivo: {e}")
            total_erros += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO DA MIGRAÇÃO")
    print("=" * 60)
    print(f"   ✅ Total migrado: {total_migrados} registros")
    print(f"   ❌ Erros: {total_erros}")
    print("=" * 60)
    
    # Mostrar estatísticas do banco
    print("\n📈 Dados no banco após migração:")
    ativos = db.listar_ativos()
    for ativo in ativos:
        print(f"   • {ativo['ativo']}: {ativo['total_registros']} registros")
    
    print("\n✅ Migração concluída!")


if __name__ == "__main__":
    migrar_csv_para_sqlite()