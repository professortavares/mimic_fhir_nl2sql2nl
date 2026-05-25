# mimic_fhir_nl2sql2nl

## O que é NL2SQL2NL?

NL2SQL2NL é uma solução que automatiza a interação com bancos de dados através de linguagem natural. O fluxo funciona da seguinte forma:

1. **NL (Natural Language)** → Usuário faz uma pergunta em português
2. **SQL** → Um modelo de IA (LLM) converte a pergunta em uma consulta SQL
3. **Execução** → A consulta SQL é executada no banco de dados
4. **NL (Natural Language)** → O resultado é convertido de volta para uma resposta em linguagem natural

Este projeto implementa uma solução NL2SQL2NL para dados do **MIMIC FHIR**, um banco de dados de registros eletrônicos de saúde, usando **LangChain**, **LangGraph** e modelos da **OpenAI**.

---

## Pré-requisitos

- **Docker** e **Docker Compose** instalados
- **Banco de dados Postgres** acessível na máquina hospedeira em `localhost:5432`
- **Chave de API da OpenAI** (obtenha em https://platform.openai.com/api-keys)

---

## Configuração

### Passo 1: Copiar variáveis de ambiente

```bash
cp .env.example .env
```

### Passo 2: Preencher variáveis no `.env`

Edite o arquivo `.env` com suas credenciais:

```dotenv
# Host do Postgres (use 'host.docker.internal' dentro do Docker, 'localhost' localmente)
POSTGRES_HOST=host.docker.internal

# Porta padrão do Postgres
POSTGRES_PORT=5432

# Nome do banco de dados
POSTGRES_DB=app_mimic_fhir

# Usuário do banco
POSTGRES_USER=app_mimic_fhir

# Senha do banco
POSTGRES_PASSWORD=app_mimic_fhir

# Chave de API da OpenAI (obrigatório)
OPENAI_API_KEY=sk-proj-...
```

**Nota:** Se você executar os testes e scripts localmente (fora do Docker), use `POSTGRES_HOST=localhost`. Se usar Docker Compose, use `POSTGRES_HOST=host.docker.internal`.

---

## Como executar

### Via Docker Compose (Recomendado)

```bash
docker compose up --build
```

Após alguns minutos, abra um navegador em:

```
http://localhost:8888/?token=dev
```

JupyterLab estará pronto para usar. O token padrão é `dev`.

### Localmente (sem Docker)

Requer Python 3.11+:

```bash
pip install -r requirements.txt
```

Para iniciar JupyterLab localmente:

```bash
jupyter lab
```

Para rodar testes:

```bash
pytest tests/ -v
```

---

## Estrutura do Projeto

```
mimic_fhir_nl2sql2nl/
├── src/nl2sql2nl/              # Pacote principal
│   ├── logger.py               # Configuração de logging
│   ├── config.py               # Carregamento de .env
│   ├── database.py             # Acesso a Postgres
│   ├── llm.py                  # Integração com OpenAI via LangChain
│   ├── pipeline.py             # Pipeline LangGraph (scaffolding)
│   └── __init__.py
├── notebooks/
│   ├── 01_teste_openai.ipynb   # Teste simples com OpenAI
│   └── 02_teste_postgres.ipynb # Teste de conexão Postgres
├── tests/
│   ├── test_config.py          # Testes de carregamento de config
│   ├── test_database.py        # Testes de acesso ao DB
│   ├── test_llm.py             # Testes de LLM
│   └── conftest.py             # Configuração pytest
├── Dockerfile                  # Imagem Docker
├── docker-compose.yml          # Orquestração Docker
├── requirements.txt            # Dependências Python
├── .env                        # Variáveis de ambiente (não commitar)
├── .env.example                # Modelo de .env
└── README.md                   # Este arquivo
```

---

## Notebooks Disponíveis

### 1. `01_teste_openai.ipynb`

Demonstra como usar LangChain para fazer uma chamada simples ao modelo GPT-4o-mini da OpenAI:
- Carrega as configurações de ambiente
- Cria uma instância do modelo
- Envia uma pergunta e obtém uma resposta
- Exemplo de chamada direta via LangChain

**Como usar:** Abra em JupyterLab e execute todas as células sequencialmente.

### 2. `02_teste_postgres.ipynb`

Testa a conectividade com o banco PostgreSQL e executa uma query MIMIC FHIR:
- Verifica a conexão com o banco
- Executa a consulta especificada no projeto
- Exibe os resultados em formato tabular (DataFrame)

**Como usar:** Abra em JupyterLab e execute todas as células sequencialmente.

---

## Testes Unitários

Os testes cobrem os módulos principais e usam mocks para evitar dependências externas (Postgres, OpenAI).

```bash
# Rodar todos os testes
pytest tests/ -v

# Rodar com cobertura
pytest tests/ --cov=src/nl2sql2nl --cov-report=html

# Rodar teste específico
pytest tests/test_llm.py -v
```

Todos os testes devem passar. Se algum falhar, verifique se as variáveis de ambiente estão definidas em `.env`.

---

## Stack Tecnológico

| Componente | Versão | Propósito |
|---|---|---|
| Python | 3.11 | Runtime |
| LangChain | ~0.3 | Framework para LLM |
| LangGraph | ~0.2 | Orquestração de agentes |
| OpenAI API | (via langchain-openai) | Modelo GPT-4o-mini |
| Psycopg2 | ~2.9 | Driver Postgres |
| Pytest | ~8.0 | Testes unitários |
| Pandas | ~2.0 | Análise de dados |
| Jupyter | (via base-notebook) | Notebooks interativos |

---

## Roadmap — Evolução Futura

O scaffolding atual (Sprint 01) estabelece a base. Próximas sprints incluem:

- **Sprint 02:** Implementar nós do pipeline LangGraph com prompts para geração SQL
- **Sprint 03:** Adicionar validação de SQL e tratamento de erros de query
- **Sprint 04:** Integrar feedback e refinamento de respostas
- **Sprint 05+:** Testes de ponta-a-ponta, otimizações e documentação

O arquivo `src/nl2sql2nl/pipeline.py` contém TODOs que marcar os próximos passos.

---

## Troubleshooting

### Erro: `Connection refused` ao rodar testes

Certifique-se de que as variáveis de ambiente estão definidas. O `tests/conftest.py` define defaults para testes (mock database), então se o erro persiste, verifique se `OPENAI_API_KEY` está preenchida no `.env`.

### Erro: `ModuleNotFoundError: No module named 'nl2sql2nl'`

Se executar notebooks localmente, as células iniciais fazem `sys.path.insert(0, "src")`. Se estiver usando Docker, o `src/` já está no PYTHONPATH.

### Erro: `POSTGRES_HOST` não alcança o banco

- **Dentro do Docker:** Use `POSTGRES_HOST=host.docker.internal`
- **Localmente:** Use `POSTGRES_HOST=localhost`
- **Verifique:** O Postgres está rodando em `localhost:5432`?

### JupyterLab não abre em `http://localhost:8888`

- Verifique se o container está rodando: `docker ps | grep jupyter`
- Veja os logs: `docker compose logs jupyterlab`
- Reinicie: `docker compose down && docker compose up`

---

## Contribuindo

1. Crie uma branch para seu trabalho: `git checkout -b feature/sua-feature`
2. Faça commits descritivos em português
3. Abra um pull request explicando as mudanças
4. Certifique-se de que testes passam: `pytest tests/`

---

## Licença

Este projeto é distribuído sob a licença especificada no arquivo [LICENSE](LICENSE).

---

## Contato

Para dúvidas ou sugestões, abra uma issue no repositório.