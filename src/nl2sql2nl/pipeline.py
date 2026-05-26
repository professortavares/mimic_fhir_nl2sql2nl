"""
Módulo de pipeline NL2SQL2NL usando LangGraph.

Este módulo define o grafo de processamento:
  1. interpretar_pergunta  — recebe a pergunta em linguagem natural
  2. gerar_sql             — converte para SQL usando o LLM
  3. executar_sql          — executa no Postgres
  4. formatar_resposta     — converte resultado em linguagem natural

Status: scaffolding inicial — os nós retornam valores de exemplo.
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from nl2sql2nl.logger import obter_logger

logger = obter_logger(__name__)


class EstadoPipeline(TypedDict):
    """Estado compartilhado entre os nós do pipeline."""
    pergunta: str
    sql_gerado: str
    resultados: list
    resposta_final: str


def interpretar_pergunta(estado: EstadoPipeline) -> EstadoPipeline:
    """Nó 1: Recebe e loga a pergunta do usuário."""
    logger.info("Pergunta recebida: %s", estado["pergunta"])
    return estado


def gerar_sql(estado: EstadoPipeline) -> EstadoPipeline:
    """Nó 2: Gera SQL a partir da pergunta (TODO: implementar com LLM)."""
    logger.info("Gerando SQL para a pergunta (scaffolding).")
    estado["sql_gerado"] = "SELECT 1;  -- placeholder"
    return estado


def executar_sql(estado: EstadoPipeline) -> EstadoPipeline:
    """Nó 3: Executa o SQL no banco (TODO: usar database.executar_consulta)."""
    logger.info("Executando SQL (scaffolding).")
    estado["resultados"] = []
    return estado


def formatar_resposta(estado: EstadoPipeline) -> EstadoPipeline:
    """Nó 4: Formata o resultado em linguagem natural (TODO: implementar com LLM)."""
    logger.info("Formatando resposta (scaffolding).")
    estado["resposta_final"] = "Resposta não implementada neste sprint."
    return estado


def construir_pipeline() -> StateGraph:
    """
    Constrói e compila o grafo de processamento NL2SQL2NL.

    Returns:
        Grafo compilado pronto para invocação.
    """
    grafo = StateGraph(EstadoPipeline)

    grafo.add_node("interpretar_pergunta", interpretar_pergunta)
    grafo.add_node("gerar_sql", gerar_sql)
    grafo.add_node("executar_sql", executar_sql)
    grafo.add_node("formatar_resposta", formatar_resposta)

    grafo.set_entry_point("interpretar_pergunta")
    grafo.add_edge("interpretar_pergunta", "gerar_sql")
    grafo.add_edge("gerar_sql", "executar_sql")
    grafo.add_edge("executar_sql", "formatar_resposta")
    grafo.add_edge("formatar_resposta", END)

    return grafo.compile()
