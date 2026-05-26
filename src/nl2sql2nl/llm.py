"""
Módulo de integração com o modelo de linguagem via LangChain e OpenAI.
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from nl2sql2nl.config import OPENAI_API_KEY
from nl2sql2nl.logger import obter_logger

logger = obter_logger(__name__)

MODELO_PADRAO = "gpt-4o-mini"


def criar_modelo(modelo: str = MODELO_PADRAO, temperatura: float = 0.0) -> ChatOpenAI:
    """
    Instancia o modelo de linguagem via LangChain.

    Args:
        modelo: Nome do modelo OpenAI a utilizar.
        temperatura: Temperatura para geração (0.0 = determinístico).

    Returns:
        Instância configurada de ChatOpenAI.
    """
    logger.info("Criando modelo LLM: %s (temperatura=%.1f)", modelo, temperatura)
    return ChatOpenAI(
        model=modelo,
        temperature=temperatura,
        api_key=OPENAI_API_KEY,
    )


def chamar_modelo(pergunta: str, modelo: str = MODELO_PADRAO) -> str:
    """
    Envia uma pergunta ao modelo e retorna a resposta em texto.

    Args:
        pergunta: Texto da pergunta a enviar ao modelo.
        modelo: Nome do modelo a utilizar.

    Returns:
        Texto da resposta do modelo.
    """
    logger.info("Enviando pergunta ao modelo '%s'.", modelo)
    llm = criar_modelo(modelo=modelo)
    mensagem = HumanMessage(content=pergunta)
    resposta = llm.invoke([mensagem])
    logger.info("Resposta recebida com %d caracteres.", len(resposta.content))
    return resposta.content
