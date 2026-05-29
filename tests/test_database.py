"""
Testes unitários para o módulo database.
"""
import pytest
from unittest.mock import patch, MagicMock
from nl2sql2nl.database import criar_conexao, executar_consulta


class TestCriarConexao:
    """Testa criação de conexão com o banco."""

    @patch("nl2sql2nl.database.psycopg2.connect")
    def test_conexao_bem_sucedida(self, mock_connect):
        """Deve chamar psycopg2.connect com os parâmetros corretos."""
        mock_conexao = MagicMock()
        mock_connect.return_value = mock_conexao

        resultado = criar_conexao()

        assert mock_connect.called
        assert resultado == mock_conexao

    @patch("nl2sql2nl.database.psycopg2.connect")
    def test_erro_de_conexao_propaga_excecao(self, mock_connect):
        """Deve propagar OperationalError quando a conexão falha."""
        import psycopg2
        mock_connect.side_effect = psycopg2.OperationalError("host não encontrado")

        with pytest.raises(psycopg2.OperationalError):
            criar_conexao()


class TestExecutarConsulta:
    """Testa execução de consultas SQL."""

    @patch("nl2sql2nl.database.psycopg2.connect")
    def test_retorna_lista_de_dicionarios(self, mock_connect):
        """Deve retornar lista de dicionários com os resultados."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{"id": 1, "nome": "Teste"}]
        mock_cursor.__enter__ = lambda s: s
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conexao = MagicMock()
        mock_conexao.cursor.return_value = mock_cursor
        mock_conexao.closed = False
        mock_connect.return_value = mock_conexao

        resultados = executar_consulta("SELECT 1")
        assert isinstance(resultados, list)

    @patch("nl2sql2nl.database.psycopg2.connect")
    def test_executa_com_parametros(self, mock_connect):
        """Deve passar parâmetros para o SQL."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_cursor.__enter__ = lambda s: s
        mock_cursor.__exit__ = MagicMock(return_value=False)

        mock_conexao = MagicMock()
        mock_conexao.cursor.return_value = mock_cursor
        mock_conexao.closed = False
        mock_connect.return_value = mock_conexao

        sql = "SELECT * FROM pacientes WHERE id = %s"
        executar_consulta(sql, (1,))

        mock_cursor.execute.assert_called_with(sql, (1,))
