"""
Pacote nl2sql2nl — solução NL2SQL2NL para dados MIMIC FHIR.
"""
from nl2sql2nl.pipeline import construir_pipeline
from nl2sql2nl.llm import chamar_modelo
from nl2sql2nl.database import executar_consulta

__all__ = ["construir_pipeline", "chamar_modelo", "executar_consulta"]
