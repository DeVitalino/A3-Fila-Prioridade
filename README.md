# Fila de Banco com Prioridade (A3)

Projeto da avaliação A3 (Filas de Prioridade). Simula uma agência bancária com três categorias de cliente (prioritário, VIP e comum), vários guichês e um relógio simulado. Usa um heap binário implementado pelo grupo, aging, cota rotativa, SLA e detecção de starvation, e gera um log de auditoria em SQL.

Stack escolhida: **A (Python com Streamlit)**.

## Estrutura do repositório

```
python/    código-fonte, testes e README de execução
sql/       schema.sql e logs_exemplo.sql
docs/      relatório, dicionário, UML, plano de commits, roteiro e perguntas
```

## Execução rápida

```bash
cd python
pip install -r requirements.txt
streamlit run app.py
pytest
```

Detalhes em `python/README.md`.

## Documentos

| Arquivo | Conteúdo |
|---|---|
| `docs/01-relatorio-tecnico.md` | Problema, regras de negócio, algoritmo, complexidade e resultados |
| `docs/02-dicionario.md` | Classes, métodos e estruturas de dados |
| `docs/03-diagrama-classes-python.puml` | Diagrama UML em PlantUML (imagem em `.png`) |
| `docs/04-plano-de-commits.md` | Divisão do trabalho entre os 6 integrantes |
| `docs/05-roteiro-apresentacao.md` | Roteiro de 20 minutos e passo a passo do teste de estresse |
| `docs/06-banco-de-perguntas.md` | Perguntas prováveis da arguição, com respostas |
| `sql/schema.sql` | Tabelas do banco de auditoria |
| `sql/logs_exemplo.sql` | Exemplo gerado numa execução de 30 clientes |

## Integrantes

NOME | RA:

Mateus Vitalino Jesus de Almeida - 12725148609
Silas Silva Rocha - 12724163789
Rodrigo Silva Santana - 12725143243
Jeferson dos Santos Vieira - 12725161355
José Leonardo de Almeida Santos - 12725217611

