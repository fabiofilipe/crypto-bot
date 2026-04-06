import sqlite3
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime
try:
    # Quando o pacote é importado normalmente (python -m src...), o import relativo funciona
    from ..utils.logger import configurar_logger
except Exception:
    # Quando executado como script (python src/migrar_csv.py), o pacote pode não estar definido
    # Nesse caso tentamos o import absoluto a partir do diretório `src` presente em sys.path
    from utils.logger import configurar_logger


class DatabaseManager:
    """Gerenciador de conexões e operações com SQLite"""
    
    def __init__(self, db_path='data/precos_cripto.db'):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger = configurar_logger('database')
        self._inicializar_banco()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões seguras"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Permite acesso por nome de coluna
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Erro na transação: {e}")
            raise
        finally:
            conn.close()
    
    def _inicializar_banco(self):
        """Cria tabelas se não existirem"""
        self.logger.info("Inicializando banco de dados")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela principal de preços
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS precos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ativo TEXT NOT NULL,
                    preco REAL NOT NULL,
                    moeda TEXT NOT NULL,
                    horario_coleta TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Índices para otimizar consultas
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_ativo 
                ON precos(ativo)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_horario 
                ON precos(horario_coleta)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_ativo_horario 
                ON precos(ativo, horario_coleta)
            """)
            
            self.logger.info("Banco de dados inicializado com sucesso")
    
    def inserir_preco(self, ativo, preco, moeda, horario_coleta):
        """Insere um novo registro de preço"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO precos (ativo, preco, moeda, horario_coleta)
                    VALUES (?, ?, ?, ?)
                """, (ativo, preco, moeda, horario_coleta))
                
                self.logger.debug(f"Registro inserido: {ativo} - {preco} {moeda}")
                return cursor.lastrowid
                
        except Exception as e:
            self.logger.error(f"Erro ao inserir preço: {e}")
            return None
    
    def obter_ultimo_preco(self, ativo):
        """Obtém o último preço registrado de um ativo"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM precos 
                    WHERE ativo = ? 
                    ORDER BY horario_coleta DESC 
                    LIMIT 1
                """, (ativo,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            self.logger.error(f"Erro ao obter último preço: {e}")
            return None
    
    def obter_historico(self, ativo, limite=100):
        """Obtém histórico de preços de um ativo"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM precos 
                    WHERE ativo = ? 
                    ORDER BY horario_coleta DESC 
                    LIMIT ?
                """, (ativo, limite))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Erro ao obter histórico: {e}")
            return []
    
    def obter_estatisticas(self, ativo, dias=7):
        """Obtém estatísticas de um ativo nos últimos N dias"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_registros,
                        MIN(preco) as preco_minimo,
                        MAX(preco) as preco_maximo,
                        AVG(preco) as preco_medio,
                        MIN(horario_coleta) as primeira_coleta,
                        MAX(horario_coleta) as ultima_coleta
                    FROM precos 
                    WHERE ativo = ? 
                    AND horario_coleta >= datetime('now', '-' || ? || ' days')
                """, (ativo, dias))
                
                row = cursor.fetchone()
                return dict(row) if row else None
                
        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return None
    
    def listar_ativos(self):
        """Lista todos os ativos registrados"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT DISTINCT ativo, COUNT(*) as total_registros
                    FROM precos 
                    GROUP BY ativo
                    ORDER BY ativo
                """)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Erro ao listar ativos: {e}")
            return []