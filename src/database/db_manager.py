"""
Database manager com PostgreSQL, connection pooling e query caching
"""

import os
import time
import hashlib
import json
from contextlib import contextmanager
from datetime import datetime
from typing import Optional
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

from utils.logger import configurar_logger

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
from psycopg2 import sql
from psycopg2 import pool as pg_pool


# ── Query Cache ─────────────────────────────────────────────

class QueryCache:
    """Cache de resultados de query com TTL"""

    def __init__(self, default_ttl: int = 60, max_size: int = 256):
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._store: dict[str, tuple] = {}

    def _key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        raw = json.dumps({"fn": func_name, "args": args, "kwargs": kwargs}, sort_keys=True, default=str)
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, key: str):
        if key in self._store:
            value, expires_at = self._store[key]
            if time.time() < expires_at:
                return value
            del self._store[key]
        return None

    def set(self, key: str, value, ttl: int = None) -> None:
        if len(self._store) >= self.max_size:
            oldest_key = min(self._store, key=lambda k: self._store[k][1])
            del self._store[oldest_key]
        ttl = ttl or self.default_ttl
        self._store[key] = (value, time.time() + ttl)

    def clear(self) -> None:
        self._store.clear()


_cache = QueryCache(default_ttl=60, max_size=256)


def cached(ttl: int = None):
    """Decorator para cachear resultado de funções"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = _cache.key(func.__name__, args, kwargs)
            result = _cache.get(key)
            if result is not None:
                return result
            result = func(*args, **kwargs)
            _cache.set(key, result, ttl=ttl)
            return result
        return wrapper
    return decorator


class DatabaseManager:
    """Gerenciador de conexões e operações com PostgreSQL"""

    _pool: Optional[pg_pool.SimpleConnectionPool] = None

    def __init__(self, db_url: Optional[str] = None, min_conn: int = 2, max_conn: int = 20):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError(
                "DATABASE_URL não configurado. "
                "Defina no .env: postgresql://user:password@host:port/dbname"
            )
        self.logger = configurar_logger("database")
        self.min_conn = min_conn
        self.max_conn = max_conn
        self._inicializar_pool()
        self._inicializar_banco()

    def _inicializar_pool(self):
        """Inicializa connection pool singleton"""
        if DatabaseManager._pool is None:
            try:
                DatabaseManager._pool = pg_pool.SimpleConnectionPool(
                    minconn=self.min_conn,
                    maxconn=self.max_conn,
                    dsn=self.db_url
                )
                self.logger.info(f"Connection pool criado: {self.min_conn}-{self.max_conn} conexões")
            except Exception as e:
                self.logger.warning(f"Não foi possível criar pool (usando conexão direta): {e}")
                DatabaseManager._pool = None

    @contextmanager
    def get_connection(self):
        """Context manager para conexões seguras (usa pool se disponível)"""
        if DatabaseManager._pool:
            conn = DatabaseManager._pool.getconn()
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                self.logger.error(f"Erro na transação: {e}")
                raise
            finally:
                DatabaseManager._pool.putconn(conn)
        else:
            conn = psycopg2.connect(self.db_url)
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                self.logger.error(f"Erro na transação: {e}")
                raise
            finally:
                conn.close()

    def _executar(self, query: str, params: tuple = (), fetch=None):
        """Helper para executar queries"""
        try:
            with self.get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(query, params)
                    if fetch == "one":
                        row = cur.fetchone()
                        return dict(row) if row else None
                    elif fetch == "all":
                        return [dict(r) for r in cur.fetchall()]
                    elif fetch == "count":
                        return cur.rowcount
                    return None
        except Exception as e:
            self.logger.error(f"Erro na query: {e}\n{query}")
            if fetch in ("one", "all"):
                return None if fetch == "one" else []
            return None

    def _inicializar_banco(self):
        """Cria tabelas e índices se não existirem"""
        self.logger.info("Inicializando banco de dados PostgreSQL")

        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Tabela principal de preços (expandida)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS precos (
                        id SERIAL PRIMARY KEY,
                        ativo TEXT NOT NULL,
                        preco NUMERIC(20, 8) NOT NULL,
                        moeda TEXT NOT NULL,
                        horario_coleta TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Índices
                cur.execute("CREATE INDEX IF NOT EXISTS idx_ativo ON precos(ativo)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_horario ON precos(horario_coleta)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_ativo_horario ON precos(ativo, horario_coleta)")

                # Tabela de ativos (metadata)
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS ativos (
                        simbolo TEXT PRIMARY KEY,
                        nome TEXT NOT NULL,
                        par TEXT NOT NULL,
                        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Tabela de configurações de alerta por usuário
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS alertas_config (
                        id SERIAL PRIMARY KEY,
                        canal_id BIGINT,
                        usuario_id BIGINT,
                        ativo TEXT NOT NULL,
                        tipo_alerta TEXT NOT NULL,
                        valor NUMERIC(20, 8),
                        ativo_config BOOLEAN DEFAULT true,
                        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Tabela de histórico de alertas enviados
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS alertas_historico (
                        id SERIAL PRIMARY KEY,
                        ativo TEXT NOT NULL,
                        tipo TEXT NOT NULL,
                        preco_anterior NUMERIC(20, 8),
                        preco_atual NUMERIC(20, 8),
                        variacao NUMERIC(10, 4),
                        mensagem TEXT,
                        enviado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                self.logger.info("PostgreSQL inicializado com sucesso")

    # ── Inserção ────────────────────────────────────────────

    def inserir_preco(self, ativo: str, preco: float, moeda: str, horario_coleta: str):
        """Insere um novo registro de preço"""
        return self._executar(
            "INSERT INTO precos (ativo, preco, moeda, horario_coleta) VALUES (%s, %s, %s, %s)",
            (ativo, preco, moeda, horario_coleta),
            fetch="count",
        )

    def inserir_lote(self, registros: list[dict]) -> int:
        """Insere múltiplos registros em uma única operação (batch insert)"""
        if not registros:
            return 0
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    values = [
                        (r["ativo"], r["preco"], r["moeda"], r["horario_coleta"])
                        for r in registros
                    ]
                    execute_batch(
                        cur,
                        "INSERT INTO precos (ativo, preco, moeda, horario_coleta) VALUES (%s, %s, %s, %s)",
                        values,
                    )
            self.logger.info(f"Batch insert: {len(registros)} registros inseridos")
            return len(registros)
        except Exception as e:
            self.logger.error(f"Erro no batch insert: {e}")
            return 0

    def invalidate_cache(self):
        """Limpa o cache de queries (usar após inserts)"""
        _cache.clear()

    # ── Consultas ───────────────────────────────────────────

    @cached(ttl=30)
    def obter_ultimo_preco(self, ativo: str) -> Optional[dict]:
        """Obtém o último preço registrado"""
        return self._executar(
            "SELECT * FROM precos WHERE ativo = %s ORDER BY horario_coleta DESC LIMIT 1",
            (ativo,),
            fetch="one",
        )

    def obter_historico(self, ativo: str, limite: int = 100) -> list:
        """Obtém histórico de preços"""
        return self._executar(
            "SELECT * FROM precos WHERE ativo = %s ORDER BY horario_coleta DESC LIMIT %s",
            (ativo, limite),
            fetch="all",
        )

    @cached(ttl=60)
    def obter_estatisticas(self, ativo: str, dias: int = 7) -> Optional[dict]:
        """Estatísticas de um ativo nos últimos N dias"""
        # CORRIGIDO: INTERVAL com valor inteiro seguro (não é parâmetro SQL)
        query = f"""
            SELECT
                COUNT(*) as total_registros,
                MIN(preco)::float as preco_minimo,
                MAX(preco)::float as preco_maximo,
                AVG(preco)::float as preco_medio,
                MIN(horario_coleta) as primeira_coleta,
                MAX(horario_coleta) as ultima_coleta
            FROM precos
            WHERE ativo = %s
            AND horario_coleta >= NOW() - INTERVAL '{int(dias)} days'
            """
        return self._executar(query, (ativo,), fetch="one")

    def obter_variacao_24h(self, ativo: str) -> Optional[dict]:
        """Calcula variação nas últimas 24h"""
        return self._executar(
            """
            WITH ultimos AS (
                SELECT preco, horario_coleta
                FROM precos
                WHERE ativo = %s
                ORDER BY horario_coleta DESC
                LIMIT 2
            ),
            primeiro AS (SELECT preco FROM ultimos ORDER BY horario_coleta ASC LIMIT 1),
            ultimo AS (SELECT preco FROM ultimos ORDER BY horario_coleta DESC LIMIT 1)
            SELECT
                u.preco as preco_atual,
                p.preco as preco_24h_atras,
                CASE WHEN p.preco > 0
                    THEN ((u.preco - p.preco) / p.preco) * 100
                    ELSE 0
                END as variacao_pct
            FROM ultimo u, primeiro p
            """,
            (ativo,),
            fetch="one",
        )

    def listar_ativos(self) -> list:
        """Lista todos os ativos com contagem de registros"""
        return self._executar(
            "SELECT DISTINCT ativo, COUNT(*) as total_registros FROM precos GROUP BY ativo ORDER BY ativo",
            fetch="all",
        )

    @cached(ttl=30)
    def obter_ranking_variacao(self, horas: int = 24, limite: int = 10) -> list:
        """Ranking de ativos por variação percentual"""
        # CORRIGIDO: INTERVAL com valor inteiro seguro
        query = f"""
            WITH dados AS (
                SELECT
                    ativo,
                    FIRST_VALUE(preco) OVER (PARTITION BY ativo ORDER BY horario_coleta DESC) as preco_atual,
                    FIRST_VALUE(preco) OVER (PARTITION BY ativo ORDER BY horario_coleta ASC) as preco_antigo
                FROM precos
                WHERE horario_coleta >= NOW() - INTERVAL '{int(horas)} hours'
            )
            SELECT DISTINCT
                ativo,
                preco_atual::float,
                preco_antigo::float,
                CASE WHEN preco_antigo > 0
                    THEN ((preco_atual - preco_antigo) / preco_antigo) * 100
                    ELSE 0
                END as variacao_pct
            FROM dados
            ORDER BY variacao_pct DESC
            LIMIT {int(limite)}
            """
        return self._executar(query, fetch="all")

    @cached(ttl=30)
    def obter_resumo_mercado(self) -> list:
        """Resumo de todos os ativos com último preço e variação"""
        return self._executar(
            """
            WITH ultimos AS (
                SELECT DISTINCT ON (ativo)
                    ativo, preco, moeda, horario_coleta
                FROM precos
                ORDER BY ativo, horario_coleta DESC
            )
            SELECT u.ativo, u.preco::float, u.moeda, u.horario_coleta
            FROM ultimos u
            ORDER BY u.ativo
            """,
            fetch="all",
        )

    # ── Ativos (metadata) ──────────────────────────────────

    def registrar_ativo(self, simbolo: str, nome: str, par: str):
        """Registra metadata de um ativo"""
        return self._executar(
            """
            INSERT INTO ativos (simbolo, nome, par)
            VALUES (%s, %s, %s)
            ON CONFLICT (simbolo) DO UPDATE SET nome = EXCLUDED.nome, par = EXCLUDED.par
            """,
            (simbolo, nome, par),
            fetch="count",
        )

    def obter_info_ativo(self, simbolo: str) -> Optional[dict]:
        """Obtém informações de um ativo"""
        return self._executar(
            "SELECT * FROM ativos WHERE simbolo = %s",
            (simbolo,),
            fetch="one",
        )

    # ── Alertas persistidos ────────────────────────────────

    def salvar_alerta(self, alerta: dict):
        """Persiste alerta no histórico"""
        return self._executar(
            """
            INSERT INTO alertas_historico (ativo, tipo, preco_anterior, preco_atual, variacao, mensagem)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                alerta.get("ativo"),
                alerta.get("tipo"),
                alerta.get("preco_anterior"),
                alerta.get("preco_atual"),
                alerta.get("variacao"),
                str(alerta),
            ),
            fetch="count",
        )

    def obter_historico_alertas(self, limite: int = 20) -> list:
        """Histórico de alertas persistidos"""
        return self._executar(
            "SELECT * FROM alertas_historico ORDER BY enviado_em DESC LIMIT %s",
            (limite,),
            fetch="all",
        )

    # ── Conversão de moeda ─────────────────────────────────

    def obter_taxa_conversao(self, de: str = "USD", para: str = "BRL") -> Optional[float]:
        """Placeholder - taxa pode ser armazenada em tabela dedicada"""
        # Por enquanto retorna hardcoded ou de cache
        # No futuro, buscar da API e salvar em tabela 'taxas_conversao'
        taxas_padrao = {("USD", "BRL"): 5.0}
        return taxas_padrao.get((de, para))
