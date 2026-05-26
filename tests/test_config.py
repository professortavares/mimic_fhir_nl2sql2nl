"""
Testes unitários para o módulo config.
"""
import pytest
from unittest.mock import patch


class TestObterVariavel:
    """Testa a leitura de variáveis de ambiente."""

    def test_variavel_presente(self):
        """Deve retornar o valor quando a variável está definida."""
        with patch.dict("os.environ", {"MINHA_VAR": "valor_teste"}):
            import nl2sql2nl.config as config_mod
            resultado = config_mod._obter_variavel("MINHA_VAR")
            assert resultado == "valor_teste"

    def test_variavel_ausente_lanca_erro(self):
        """Deve lançar EnvironmentError quando a variável não está definida."""
        with patch.dict("os.environ", {}, clear=True):
            import importlib
            import nl2sql2nl.config as config_mod
            with pytest.raises(EnvironmentError):
                config_mod._obter_variavel("VAR_INEXISTENTE")

    def test_porta_postgres_padrao(self):
        """Porta Postgres deve ser inteiro."""
        import nl2sql2nl.config as config_mod
        assert isinstance(config_mod.POSTGRES_PORT, int)

    def test_postgres_host_carregado(self):
        """Host Postgres deve estar carregado."""
        import nl2sql2nl.config as config_mod
        assert config_mod.POSTGRES_HOST is not None
        assert len(config_mod.POSTGRES_HOST) > 0

    def test_openai_api_key_carregado(self):
        """OpenAI API Key deve estar carregada."""
        import nl2sql2nl.config as config_mod
        assert config_mod.OPENAI_API_KEY is not None
        assert len(config_mod.OPENAI_API_KEY) > 0
