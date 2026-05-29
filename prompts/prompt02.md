[C — Contextualizado]
Estou construindo uma solução NL2SQL2NL em Python. O fluxo esperado é: usuário faz uma pergunta em português → uma LLM transforma a pergunta em SQL usando os metadados de `/dic/dicionario_dados.yaml` → o SQL é executado no Postgres → outra chamada simples de LLM transforma o resultado em texto em linguagem natural.

[L — Limitado]
Implemente este fluxo no notebook `notebooks/03_nl2sql2nl.ipynb`. Use apenas chamadas simples com LangChain e OpenAI, sem LangGraph neste momento. O código deve ser em português, simples de entender, com docstrings, comentários de linha relevantes e logs para fluxo normal, erros e falhas. Use variáveis do `.env`.

[A — Acionável]
Crie ou atualize o notebook `notebooks/03_nl2sql2nl.ipynb` para executar o fluxo completo:
1. carregar variáveis do `.env`;
2. carregar o dicionário `/dic/dicionario_dados.yaml`;
3. receber uma pergunta em português;
4. gerar SQL via LangChain/OpenAI usando o dicionário de dados como contexto;
5. executar a SQL no Postgres;
6. converter o resultado em resposta final em português via LangChain/OpenAI;
7. exibir a pergunta, SQL gerada, resultado bruto e resposta final.

[R — Referenciado]
Use como teste esta pergunta:

"Quais são os períodos dos encontros, períodos das localizações e nomes das localizações do paciente com identificador 10000032?"

A SQL gerada deve ser equivalente a:

```sql
select p.nome_familia , e.periodo_inicio , e.periodo_fim, el.periodo_inicio, el.periodo_fim, l.nome
from pacientes p inner join encontros e on p.id = e.paciente_id
inner join encontros_localizacoes el on el.encontro_id = e.id
inner join localizacoes l on el.localizacao_id = l.id
where p.identificador = '10000032'
````

[O — Objetivo]
Ao final, o notebook `03_nl2sql2nl.ipynb` deve demonstrar o fluxo completo NL2SQL2NL funcionando: pergunta em português → SQL → consulta no Postgres → resposta final em português.
