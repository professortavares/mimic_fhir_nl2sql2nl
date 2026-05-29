"""
Módulo de acesso ao banco de dados Postgres.
"""
import psycopg2
import psycopg2.extras
from contextlib import contextmanager
from typing import Generator
from nl2sql2nl.config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD
from nl2sql2nl.logger import obter_logger

logger = obter_logger(__name__)


def criar_conexao() -> psycopg2.extensions.connection:
    """
    Cria e retorna uma conexão com o banco Postgres.

    Returns:
        Conexão psycopg2 ativa.

    Raises:
        psycopg2.OperationalError: Se não for possível conectar ao banco.
    """
    logger.info("Conectando ao Postgres em %s:%s/%s", POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
    conexao = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    logger.info("Conexão estabelecida com sucesso.")
    return conexao


@contextmanager
def conexao_banco() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    Gerenciador de contexto que abre e fecha a conexão automaticamente.

    Yields:
        Conexão psycopg2 ativa.
    """
    conexao = None
    try:
        conexao = criar_conexao()
        yield conexao
    except psycopg2.Error as erro:
        logger.error("Erro de banco de dados: %s", erro)
        raise
    finally:
        if conexao and not conexao.closed:
            conexao.close()
            logger.info("Conexão encerrada.")


def executar_consulta(sql: str, parametros: tuple = ()) -> list[dict]:
    """
    Executa uma consulta SQL e retorna os resultados como lista de dicionários.

    Args:
        sql: Consulta SQL a executar.
        parametros: Parâmetros para a consulta (evita SQL injection).

    Returns:
        Lista de dicionários com os resultados.
    """
    with conexao_banco() as conexao:
        with conexao.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            logger.info("Executando consulta SQL.")
            cursor.execute(sql, parametros)
            resultados = cursor.fetchall()
            logger.info("Consulta retornou %d linhas.", len(resultados))
            return [dict(linha) for linha in resultados]
