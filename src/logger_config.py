import logging
import os
from datetime import datetime

def configurar_logger(nome_logger="projeto_otimizacao"):
    # Garante que a pasta de logs existe
    os.makedirs("logs", exist_ok=True)

    # Nome do arquivo de log com data, para não sobrescrever execuções antigas
    nome_arquivo = f"logs/execucao_{datetime.now().strftime('%Y%m%d')}.log"

    logger = logging.getLogger(nome_logger)
    logger.setLevel(logging.DEBUG)

    # Evita adicionar handlers duplicados se a função for chamada mais de uma vez
    if not logger.handlers:
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Handler de arquivo: grava tudo (DEBUG pra cima)
        file_handler = logging.FileHandler(nome_arquivo, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formato)

        # Handler de console: mostra só avisos e erros na tela
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formato)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Logger único, importável em qualquer módulo do projeto
logger = configurar_logger()