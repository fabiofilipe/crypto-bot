import logging
from pathlib import Path
from datetime import datetime


def configurar_logger(nome_modulo):
    """Configura e retorna um logger para o módulo"""
    
    # Criar diretório de logs se não existir
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Nome do arquivo de log com data
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    log_file = log_dir / f'pipeline_{data_hoje}.log'
    
    # Configurar logger
    logger = logging.getLogger(nome_modulo)
    logger.setLevel(logging.DEBUG)
    
    # Evitar duplicação de handlers
    if logger.handlers:
        return logger
    
    # Formato das mensagens
    formato = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formato)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger