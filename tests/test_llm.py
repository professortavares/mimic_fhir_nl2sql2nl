"""
Testes unitários para o módulo llm.
"""
import pytest
from unittest.mock import patch, MagicMock
from nl2sql2nl.llm import criar_modelo, chamar_modelo, MODELO_PADRAO


class TestCriarModelo:
    """Testa criação do modelo LLM."""

    def test_retorna_instancia_chat_openai(self):
        """Deve retornar uma instância de ChatOpenAI."""
        from langchain_openai import ChatOpenAI
        modelo = criar_modelo()
        assert isinstance(modelo, ChatOpenAI)

    def test_modelo_padrao_correto(self):
        """O modelo padrão deve ser gpt-4o-mini."""
        assert MODELO_PADRAO == "gpt-4o-mini"

    def test_temperatura_padrao_zero(self):
        """Temperatura padrão deve ser 0.0 (determinístico)."""
        modelo = criar_modelo()
        assert modelo.temperature == 0.0

    @patch("nl2sql2nl.llm.ChatOpenAI")
    def test_modelo_customizado(self, mock_chat_class):
        """Deve criar modelo com parâmetros customizados."""
        mock_instancia = MagicMock()
        mock_chat_class.return_value = mock_instancia

        criar_modelo(modelo="gpt-3.5-turbo", temperatura=0.7)

        mock_chat_class.assert_called_once()
        call_kwargs = mock_chat_class.call_args[1]
        assert call_kwargs["model"] == "gpt-3.5-turbo"
        assert call_kwargs["temperature"] == 0.7


class TestChamarModelo:
    """Testa invocação do modelo."""

    @patch("nl2sql2nl.llm.ChatOpenAI")
    def test_retorna_string(self, mock_chat_class):
        """Deve retornar string com o conteúdo da resposta."""
        mock_instancia = MagicMock()
        mock_resposta = MagicMock()
        mock_resposta.content = "Resposta de teste."
        mock_instancia.invoke.return_value = mock_resposta
        mock_chat_class.return_value = mock_instancia

        resultado = chamar_modelo("Pergunta teste")

        assert isinstance(resultado, str)
        assert resultado == "Resposta de teste."

    @patch("nl2sql2nl.llm.ChatOpenAI")
    def test_envia_pergunta_ao_modelo(self, mock_chat_class):
        """Deve chamar invoke com a pergunta fornecida."""
        mock_instancia = MagicMock()
        mock_resposta = MagicMock()
        mock_resposta.content = "ok"
        mock_instancia.invoke.return_value = mock_resposta
        mock_chat_class.return_value = mock_instancia

        chamar_modelo("Qual é a capital do Brasil?")

        assert mock_instancia.invoke.called

    @patch("nl2sql2nl.llm.ChatOpenAI")
    def test_usa_modelo_customizado(self, mock_chat_class):
        """Deve usar o modelo customizado se fornecido."""
        mock_instancia = MagicMock()
        mock_resposta = MagicMock()
        mock_resposta.content = "ok"
        mock_instancia.invoke.return_value = mock_resposta
        mock_chat_class.return_value = mock_instancia

        chamar_modelo("pergunta", modelo="gpt-3.5-turbo")

        call_kwargs = mock_chat_class.call_args[1]
        assert call_kwargs["model"] == "gpt-3.5-turbo"
