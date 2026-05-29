"""
Módulo de configuração: carrega variáveis de ambiente do arquivo .env.
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from nl2sql2nl.logger import obter_logger

logger = obter_logger(__name__)

_raiz_projeto = Path(__file__).resolve().parents[2]
load_dotenv(_raiz_projeto / ".env")


def _obter_variavel(nome: str) -> str:
    """
    Lê uma variável de ambiente obrigatória.
    Lança EnvironmentError se não estiver definida.
    """
    valor = os.getenv(nome)
    if not valor:
        logger.error("Variável de ambiente obrigatória não encontrada: %s", nome)
        raise EnvironmentError(f"Variável de ambiente '{nome}' não configurada.")
    return valor


POSTGRES_HOST: str = _obter_variavel("POSTGRES_HOST")
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB: str = _obter_variavel("POSTGRES_DB")
POSTGRES_USER: str = _obter_variavel("POSTGRES_USER")
POSTGRES_PASSWORD: str = _obter_variavel("POSTGRES_PASSWORD")

OPENAI_API_KEY: str = _obter_variavel("OPENAI_API_KEY")

logger.info("Configurações carregadas com sucesso.")
