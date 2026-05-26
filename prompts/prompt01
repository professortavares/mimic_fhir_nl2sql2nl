[C — Contextualizado]
Estou construindo um projeto em Python para uma solução NL2SQL2NL: receber perguntas em linguagem natural, consultar um banco SQL e retornar respostas em linguagem natural.

[L — Limitado]
O projeto deve rodar via Docker e inicialmente subir um ambiente Jupyter Lab. Use código simples, em português, com docstrings e comentários de linha relevantes. Inclua LangChain, LangGraph e acesso à OpenAI via API usando variável de ambiente. Crie `.env.example` com placeholder para o segredo. Gere logs para fluxo normal, erros e falhas. Inclua testes unitários para métodos críticos.

[A — Acionável]
Crie a estrutura do projeto, o código Python, os arquivos Docker necessários, testes, notebooks e documentação.

[R — Referenciado]
Crie:
1. `README.md` explicando o propósito da solução NL2SQL2NL e como executar o projeto.
2. `.env.example` com placeholder para `OPENAI_API_KEY`.
3. Um notebook em `notebooks/` que faça uma chamada simples à OpenAI via LangChain usando o modelo `gpt5-mini`.
4. Um notebook em `notebooks/` que teste a conexão com Postgres executando:

```sql
select p.nome_familia , e.periodo_inicio , e.periodo_fim, el.periodo_inicio, el.periodo_fim, l.nome
from pacientes p inner join encontros e on p.id = e.paciente_id
inner join encontros_localizacoes el on el.encontro_id = e.id
inner join localizacoes l on el.localizacao_id = l.id
where p.identificador = '10000032'
````

[O — Objetivo]
Ao final, entregue um projeto funcional, simples de entender, executável com Docker, documentado, testado e pronto para evoluir para uma solução completa NL2SQL2NL.
