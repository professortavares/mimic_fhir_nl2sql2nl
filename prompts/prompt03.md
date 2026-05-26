[C — Contextualizado]
Estou construindo uma solução NL2SQL2NL em Python. O fluxo esperado é: usuário faz uma pergunta em português → o sistema usa o dicionário de dados em `/dic/dicionario_dados.yaml` → uma LLM planeja a consulta SQL → uma LLM gera a SQL → o sistema valida e executa a SQL no Postgres → em caso de erro, o sistema corrige a SQL e tenta novamente → ao final, uma LLM transforma o resultado em resposta em português.

[L — Limitado]
Crie o notebook `notebooks/04_nl2sql2nl_langgraph.ipynb`. Use LangGraph para orquestrar o fluxo e LangChain para chamadas simples à OpenAI. O código deve ser em português, simples de entender, com docstrings, comentários de linha relevantes e logs para fluxo normal, erros e falhas. Use variáveis do `.env`. Não exponha segredos. Limite retries de correção SQL a 3 tentativas. Permita apenas consultas `SELECT`.

[A — Acionável]
Implemente no notebook `04_nl2sql2nl_langgraph.ipynb` um fluxo LangGraph com os seguintes nós:
1. `carregar_dicionario`: lê `/dic/dicionario_dados.yaml`;
2. `planejar_sql`: usa a LLM para montar um plano curto da consulta;
3. `gerar_sql`: usa a LLM para gerar apenas a SQL;
4. `validar_sql`: bloqueia comandos não permitidos e múltiplas queries;
5. `executar_sql`: executa a SQL no Postgres e captura resultados ou erros;
6. `decidir_proximo_passo`: decide se segue para resposta final, corrige SQL ou falha;
7. `corrigir_sql`: usa a LLM para corrigir a SQL com base no erro retornado;
8. `gerar_resposta_natural`: transforma o resultado SQL em texto em português;
9. `falha_controlada`: retorna mensagem clara se exceder as tentativas.

Inclua também uma célula no notebook para exibir o grafo do LangGraph, preferencialmente usando:

```python
from IPython.display import Image, display

display(Image(grafo.get_graph().draw_mermaid_png()))
````

Se a renderização por PNG não funcionar no ambiente, exiba o Mermaid como texto usando:

```python
print(grafo.get_graph().draw_mermaid())
```

[R — Referenciado]
Use como pergunta de teste:

"Quais são os períodos dos encontros, períodos das localizações e nomes das localizações do paciente com identificador 10000032?"

A SQL gerada deve ser equivalente a:

```sql
select p.nome_familia , e.periodo_inicio , e.periodo_fim, el.periodo_inicio, el.periodo_fim, l.nome
from pacientes p inner join encontros e on p.id = e.paciente_id
inner join encontros_localizacoes el on el.encontro_id = e.id
inner join localizacoes l on el.localizacao_id = l.id
where p.identificador = '10000032'
```

Use `/dic/dicionario_dados.yaml` como fonte principal para tabelas, colunas, relacionamentos e significados de negócio.

O estado do grafo deve conter, no mínimo:

```python
{
    "pergunta": str,
    "dicionario_dados": dict,
    "plano_sql": str,
    "sql_gerado": str,
    "resultado_sql": list,
    "erro_sql": str | None,
    "tentativas": int,
    "max_tentativas": int,
    "resposta_final": str
}
```

O fluxo esperado do grafo é:

```text
START
  ↓
carregar_dicionario
  ↓
planejar_sql
  ↓
gerar_sql
  ↓
validar_sql
  ↓
executar_sql
  ↓
decidir_proximo_passo
    ├── corrigir_sql → validar_sql
    ├── gerar_resposta_natural → END
    └── falha_controlada → END
```

[O — Objetivo]
Ao final, o notebook `04_nl2sql2nl_langgraph.ipynb` deve demonstrar o fluxo completo NL2SQL2NL com LangGraph: carregar metadados, planejar SQL, gerar SQL, validar, executar no Postgres, corrigir erros com retries, gerar resposta final em português e exibir visualmente o grafo no notebook.
