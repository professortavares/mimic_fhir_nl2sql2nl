"""
Módulo de configuração de logging para o projeto NL2SQL2NL.
"""
import logging
import sys


def obter_logger(nome: str) -> logging.Logger:
    """
    Cria e configura um logger com o nome fornecido.

    Args:
        nome: Nome do logger (geralmente __name__ do módulo chamador).

    Returns:
        Logger configurado com handler de saída no console.
    """
    logger = logging.getLogger(nome)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formato)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
