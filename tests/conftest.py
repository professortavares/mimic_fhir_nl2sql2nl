"""
Configurações compartilhadas para os testes.
Define variáveis de ambiente necessárias antes da importação dos módulos.
"""
import os

os.environ.setdefault("POSTGRES_HOST", "localhost")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_pass")
os.environ.setdefault("OPENAI_API_KEY", "sk-test-fake-key")
