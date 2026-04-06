import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import time
try:
    # Preferir imports relativos quando o pacote estiver configurado
    from ..utils.logger import configurar_logger
    from ..database.db_manager import DatabaseManager
except Exception:
    # Fallback para execução como script (python src/migrar_csv.py)
    from utils.logger import configurar_logger
    from database.db_manager import DatabaseManager


class ColetorBase:
    """Classe base para todos os coletores de dados financeiros"""
    
    def __init__(self, nome_ativo, url_api, max_tentativas=3, timeout=10, usar_db=True):
        self.nome_ativo = nome_ativo
        self.url_api = url_api
        self.max_tentativas = max_tentativas
        self.timeout = timeout
        self.usar_db = usar_db
        
        # Diretório para CSVs (backup)
        self.data_dir = Path('data/raw')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar logger
        self.logger = configurar_logger(f'coletor.{nome_ativo.lower()}')
        
        # Inicializar banco de dados
        if self.usar_db:
            self.db = DatabaseManager()
    
    def coletar(self):
        """Método que deve ser implementado por cada coletor"""
        raise NotImplementedError("Subclasse deve implementar o método coletar()")
    
    def fazer_requisicao(self):
        """Faz a requisição HTTP com retry automático"""
        for tentativa in range(1, self.max_tentativas + 1):
            try:
                self.logger.debug(f"Tentativa {tentativa}/{self.max_tentativas} - GET {self.url_api}")
                
                response = requests.get(self.url_api, timeout=self.timeout)
                response.raise_for_status()
                
                self.logger.debug(f"Resposta recebida: Status {response.status_code}")
                return response.json()
                
            except requests.exceptions.Timeout:
                self.logger.warning(f"Timeout na tentativa {tentativa}/{self.max_tentativas}")
                if tentativa < self.max_tentativas:
                    time.sleep(2 * tentativa)
                    
            except requests.exceptions.HTTPError as e:
                self.logger.error(f"Erro HTTP {e.response.status_code}: {e}")
                if e.response.status_code >= 500 and tentativa < self.max_tentativas:
                    time.sleep(2 * tentativa)
                else:
                    break
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Erro na requisição: {e}")
                if tentativa < self.max_tentativas:
                    time.sleep(2 * tentativa)
        
        self.logger.error(f"Falha após {self.max_tentativas} tentativas")
        return None
    
    def validar_dados(self, dados):
        """Valida se os dados coletados são válidos"""
        if not dados:
            self.logger.error("Dados vazios ou None")
            return False
        
        campos_obrigatorios = ['ativo', 'preco', 'moeda', 'horario_coleta']
        for campo in campos_obrigatorios:
            if campo not in dados:
                self.logger.error(f"Campo obrigatório ausente: {campo}")
                return False
            
            if dados[campo] is None or dados[campo] == '':
                self.logger.error(f"Campo {campo} está vazio")
                return False
        
        # Validar se preço é numérico e positivo
        try:
            preco = float(dados['preco'])
            if preco <= 0:
                self.logger.error(f"Preço inválido: {preco}")
                return False
        except (ValueError, TypeError) as e:
            self.logger.error(f"Preço não é numérico: {e}")
            return False
        
        return True
    
    def salvar_dados(self, dados):
        """Salva dados no banco de dados e opcionalmente em CSV"""
        if not self.validar_dados(dados):
            return False
        
        sucesso = True
        
        # Salvar no banco de dados
        if self.usar_db:
            try:
                id_inserido = self.db.inserir_preco(
                    ativo=dados['ativo'],
                    preco=dados['preco'],
                    moeda=dados['moeda'],
                    horario_coleta=dados['horario_coleta']
                )
                
                if id_inserido:
                    self.logger.info(f"✅ Dados salvos no DB (ID: {id_inserido}): {dados['preco']} {dados['moeda']}")
                else:
                    self.logger.error("Falha ao salvar no banco de dados")
                    sucesso = False
                    
            except Exception as e:
                self.logger.error(f"Erro ao salvar no banco: {e}")
                sucesso = False
        
        # Salvar CSV como backup
        try:
            self._salvar_csv_backup(dados)
        except Exception as e:
            self.logger.warning(f"Falha ao salvar backup CSV: {e}")
        
        return sucesso
    
    def _salvar_csv_backup(self, dados):
        """Salva CSV como backup (método privado)"""
        df = pd.DataFrame([dados])
        arquivo = self.data_dir / f'preco_{self.nome_ativo.lower()}.csv'
        
        file_exists = arquivo.exists()
        
        df.to_csv(
            arquivo, 
            mode='a', 
            header=not file_exists, 
            index=False
        )
        
        self.logger.debug(f"Backup CSV salvo: {arquivo}")
    
    def executar(self):
        """Executa o fluxo completo de coleta"""
        self.logger.info(f"Iniciando coleta de {self.nome_ativo}")
        
        try:
            dados = self.coletar()
            if dados:
                return self.salvar_dados(dados)
            else:
                self.logger.error("Coleta retornou dados vazios")
                return False
                
        except Exception as e:
            self.logger.error(f"Erro inesperado na coleta: {e}", exc_info=True)
            return False