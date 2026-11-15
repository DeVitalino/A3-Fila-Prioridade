# 🏦 Fila Bancária com 4 Níveis de Prioridade (A3)

Projeto da avaliação A3 sobre **Filas de Prioridade com Aging**. Simula uma agência bancária com quatro níveis de prioridade baseados em idade e deficiência, implementando algoritmo de envelhecimento (aging) com multiplicador 1.6, cota rotativa, monitoramento de SLA e auditoria SQL completa.

**Stack:** Python + Streamlit + Heap Binário implementado manualmente

---

## 📊 Sistema de 4 Níveis de Prioridade

O sistema classifica os clientes em quatro níveis baseados em **idade** e **presença de deficiência**:

| Nível | Perfil | Pontuação Inicial | Distribuição |
|-------|--------|------------------:|------------:|
| **Nível 4** | 80 anos ou mais | Prioridade ABSOLUTA | 1% (RARO) |
| **Nível 3** | 60 a 79 anos | 3 | 12% |
| **Nível 2** | Pessoas com deficiência | 2 | 10% |
| **Nível 1** | Sem prioridade especial | 1 | 77% |

### Prioridade Absoluta (Nível 4)

Clientes com **80 anos ou mais** têm prioridade absoluta:
- ✅ Sempre permanecem à frente de todas as outras categorias
- ✅ Não são afetados pelo algoritmo de aging
- ✅ Não podem ser ultrapassados por outros clientes
- ✅ Geração aleatória rara (1%)
- ✅ Identificação visual destacada (👑)

---

## ⏰ Algoritmo de Aging (Envelhecimento)

Para evitar **starvation** (inanição), o sistema implementa aging com **multiplicador fixo de 1.6**:

### Fórmula

```
pontuacao_atual = pontuacao_inicial × 1,6ⁿ
```

Onde:
- **pontuacao_inicial**: nível de prioridade (1, 2 ou 3)
- **1,6**: multiplicador fixo
- **n**: quantidade de períodos completos de **20 minutos** aguardados

### Exemplos de Evolução

| Categoria | Inicial | Após 20 min | Após 40 min | Após 60 min | Após 80 min |
|-----------|--------:|------------:|------------:|------------:|------------:|
| Nível 3 (60-79) | 3 | 4,8 | 7,68 | 12,29 | 19,66 |
| Nível 2 (PCD) | 2 | 3,2 | 5,12 | 8,19 | 13,11 |
| Nível 1 (Comum) | 1 | 1,6 | 2,56 | 4,10 | 6,55 |

**Importante:**
- Nível 4 (80+) **NÃO** entra no cálculo (prioridade absoluta)
- Recálculo acontece a cada 5 minutos
- Quanto maior a pontuação, maior a prioridade no atendimento

---

## 🎯 Funcionalidades Principais

### Interface Streamlit com 4 Abas

1. **📋 Filas**
   - **Lista 1:** Ordem de Chegada (cronológica)
   - **Lista 2:** Ordem de Atendimento (calculada por prioridade + aging)
   - Visualização simultânea das duas ordenações

2. **🪟 Guichês**
   - Status em tempo real (livre/ocupado)
   - Cliente em atendimento
   - Tempo restante do serviço
   - Total de atendimentos por guichê

3. **📊 Atendimentos**
   - Histórico completo de atendimentos
   - Tempo de espera por cliente
   - Status do SLA (dentro/fora)
   - Motivo da chamada (NORMAL, AGING, COTA)

4. **📈 Indicadores e Auditoria**
   - Métricas por nível de prioridade
   - Tempo médio de espera
   - Percentual dentro do SLA
   - Detecção de starvation
   - Alertas de SLA
   - Exportação de logs SQL

### Mecanismos Anti-Starvation

1. **Aging (1.6x a cada 20 min)**
   - Aumenta pontuação progressivamente
   - Clientes de menor prioridade eventualmente ultrapassam os de maior prioridade

2. **Cota Rotativa**
   - Após N atendimentos prioritários seguidos
   - Garante que pelo menos 1 cliente Nível 1 seja atendido
   - Evita espera indefinida

3. **Monitoramento de SLA**
   - Alertas quando próximo de estourar
   - Registro de violações
   - Métricas por categoria

---

## 📁 Estrutura do Projeto

```
A3-Fila-Prioridade/
│
├── python/
│   ├── trabalhoA3.py                  # Ponto de entrada (execute este!)
│   ├── requirements.txt               # Dependências
│   ├── pytest.ini                     # Configuração de testes
│   │
│   ├── dominio/                       # Entidades e regras de negócio
│   │   ├── cliente.py                 # Cliente com idade e aging
│   │   ├── categoria.py               # 4 níveis de prioridade
│   │   ├── heap_binario.py            # Heap implementado manualmente
│   │   ├── guiche.py                  # Guichês de atendimento
│   │   ├── atendimento.py             # Registro de atendimento
│   │   ├── tipo_servico.py            # Catálogo de serviços
│   │   ├── configuracao.py            # Parâmetros do sistema
│   │   └── evento_fila.py             # Eventos (entrada, saída, alertas)
│   │
│   ├── servico/                       # Lógica de negócio
│   │   ├── servico_fila.py            # Gerenciamento da fila e aging
│   │   ├── gerador_clientes.py        # Geração aleatória (1%, 12%, 10%, 77%)
│   │   ├── relogio_simulado.py        # Controle de tempo simulado
│   │   └── metricas.py                # Cálculos estatísticos
│   │
│   ├── repositorio/                   # Persistência e auditoria
│   │   ├── repositorio_clientes.py
│   │   ├── repositorio_eventos.py
│   │   ├── repositorio_atendimentos.py
│   │   └── gerador_log_sql.py         # Exportação para SQL
│   │
│   ├── ui/
│   │   └── painel_streamlit.py        # Interface completa
│   │
│   └── testes/                        # Testes automatizados
│       ├── test_aging.py              # Testes do aging
│       ├── test_cota.py               # Testes da cota rotativa
│       ├── test_heap.py               # Testes do heap binário
│       ├── test_sla.py                # Testes de SLA
│       └── auxiliar.py                # Funções auxiliares
│
├── BancoDadosA3/                      # Auditoria SQL
│   ├── schema.sql                     # Estrutura do banco
│   └── logs_exemplo.sql               # Exemplo de log gerado
│
└── README.md                          # Este arquivo
```

---

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd A3-Fila-Prioridade

# 2. Entre na pasta python
cd python

# 3. (Opcional) Crie um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute o simulador
streamlit run trabalhoA3.py
```

O navegador abrirá automaticamente em `http://localhost:8501`

---

## 🧪 Executar Testes

```bash
cd python
pytest
```

Testes cobrem:
- ✅ Heap binário (inserção, remoção, reorganização)
- ✅ Algoritmo de aging (1.6x a cada 20 min)
- ✅ Cota rotativa (N prioritários → 1 comum)
- ✅ Monitoramento de SLA
- ✅ Detecção e resolução de starvation

---

## 💾 Auditoria SQL

O sistema gera logs SQL completos para auditoria:

1. **Criar banco:**
   ```sql
   mysql -u root -p < BancoDadosA3/schema.sql
   ```

2. **Exportar logs do simulador:**
   - Clique em "⬇️ Baixar logsA3.sql" na aba "Indicadores e Auditoria"

3. **Importar logs:**
   ```sql
   mysql -u root -p < logsA3.sql
   ```

### Estrutura do Banco

- **banco_dados_a3**
  - `guiches`: Cadastro de guichês
  - `clientes`: Todos os clientes (com idade)
  - `eventos_fila`: Entrada, saída, alertas SLA, starvation
  - `atendimentos`: Histórico completo de atendimentos

---

## 📚 Tecnologias Utilizadas

- **Python 3.14**
- **Streamlit 1.67+** - Interface web interativa
- **Pandas 3.1+** - Manipulação de dados
- **Pytest 9.2+** - Testes automatizados
- **MySQL 8** - Banco de dados de auditoria

---

## 👥 Integrantes do Grupo

| Nome | RA |
|------|---:|
| Mateus Vitalino Jesus de Almeida | 12725148609 |
| Silas Silva Rocha | 12724163789 |
| Rodrigo Silva Santana | 12725143243 |
| Jeferson dos Santos Vieira | 12725161355 |
| José Leonardo de Almeida Santos | 12725217611 |

---

## 📖 Conceitos Acadêmicos

Este projeto demonstra:
- ✅ **Heap Binário** (implementação própria, sem bibliotecas)
- ✅ **Filas de Prioridade** com múltiplos níveis
- ✅ **Algoritmos de Aging** para evitar starvation
- ✅ **Programação Orientada a Objetos** (camadas bem definidas)
- ✅ **Simulação de Eventos Discretos** (relógio simulado)
- ✅ **SLA e Métricas de Qualidade de Serviço**
- ✅ **Auditoria e Rastreabilidade** (logs SQL transacionais)

---

## 📜 Licença

Projeto acadêmico - Avaliação A3  
Disciplina: Algoritmos e Estruturas de Dados  
Universidade: [Nome da Universidade]  
Ano: 2026

---

**Desenvolvido com dedicação pelos alunos do curso de Tecnologia em Sistemas para Internet** 🎓
