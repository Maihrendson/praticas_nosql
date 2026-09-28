# Prática 04 - OpenF1 Data Explorer

## Visão geral

Este projeto foi desenvolvido para explorar dados de Fórmula 1 usando a API pública OpenF1, com uma interface web em Streamlit. A aplicação permite:

- selecionar um ano e uma sessão de corrida;
- visualizar detalhes da sessão;
- comparar pilotos por tempo de volta;
- consultar dados de voltas em formato tabular e gráfico;
- utilizar MongoDB como cache opcional, com fallback para a API OpenF1 e, se necessário, dados simulados.

## Autores

- Aluno: Maihrendon Cauã
- Professor: Me. Ricardo Roberto

## Objetivo da prática

A prática tem como objetivo aplicar conceitos de:

- consumo de APIs REST;
- integração com banco de dados NoSQL (MongoDB);
- desenvolvimento de dashboards interativos com Streamlit;
- manipulação e visualização de dados com Pandas e Plotly;
- uso de fallback e cache para manter a aplicação funcional mesmo sem infraestrutura externa disponível.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- MongoDB (PyMongo)
- Python-dotenv

## Estrutura do projeto

```text
praticas_nosql/
├── .gitignore
├── README.md
├── requirements.txt
├── Pratica04/
│   └── code/
│       ├── .env
│       ├── db_utils.py
│       ├── requirements.txt
│       └── streamlit_app.py
├── redis/
├── riak/
└── venv/
```

## Como funciona a aplicação

A interface principal em `streamlit_app.py` realiza o seguinte fluxo:

1. Carrega a conexão com MongoDB;
2. Busca as sessões disponíveis para o ano selecionado;
3. Seleciona uma corrida;
4. Obtém os detalhes da sessão;
5. Lista os pilotos da sessão;
6. Busca os dados de voltas de cada piloto;
7. Plota um gráfico comparativo e mostra os dados em tabela.

O módulo `db_utils.py` implementa a lógica de acesso híbrida:

- MongoDB → quando disponível;
- API OpenF1 → como fonte principal de dados;
- mock/fallback → para manter o projeto funcional em caso de indisponibilidade.

## Requisitos

- Python 3.10 ou superior
- Ambiente virtual recomendado (`venv`)
- MongoDB local opcional
- Acesso à internet para consultar a API OpenF1

## Configuração e execução

### 1. Criar o ambiente virtual

```bash
cd /caminho/para/o/projeto
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r Pratica04/code/requirements.txt
```

### 3. Executar a aplicação

```bash
cd Pratica04/code
streamlit run streamlit_app.py
```

A aplicação será aberta localmente em:

```text
http://localhost:8501
```

## Variáveis de ambiente

O projeto utiliza o arquivo `.env` dentro de `Pratica04/code` com as seguintes configurações:

```env
MONGO_URI="mongodb://localhost:27017"
OPENF1_API_URL="https://api.openf1.org/v1"
```

Essas variáveis podem ser ajustadas conforme o ambiente local.

## Observações

- Caso o MongoDB não esteja disponível, a aplicação continua funcionando consultando diretamente a API OpenF1.
- Se a API também não responder, os dados simulados do fallback permitem que a interface continue renderizando.
- O ambiente virtual (`venv/`) e arquivos temporários devem ser ignorados pelo Git, conforme configurado em `.gitignore`.

## Parte complementar: Redis e Riak

Além da prática principal com MongoDB e Streamlit, o repositório também inclui duas pastas complementares:

- `redis/`: estrutura relacionada à atividade de estudo sobre Redis, um banco de dados em memória, muito utilizado para cache, filas e armazenamento leve de chave-valor.
- `riak/`: estrutura relacionada à atividade de estudo sobre Riak, um banco de dados distribuído e tolerante a falhas, com foco em escalabilidade e disponibilidade.

Essas pastas fazem parte de uma atividade acadêmica complementar ao projeto principal, com objetivo de comparar diferentes soluções NoSQL e entender as abordagens de armazenamento distribuído e de cache em sistemas modernos.

Embora o projeto principal utilize MongoDB e OpenF1, o Redis e o Riak foram incluídos no repositório como parte da prática de NoSQL, permitindo uma comparação entre:

- MongoDB: modelo documental e uso mais direto para dados estruturados;
- Redis: armazenamento rápido em memória, ideal para cache e processamento ágil;
- Riak: solução distribuída com foco em disponibilidade e tolerância a falhas.

Essas atividades complementares ajudam a ampliar o entendimento de arquiteturas NoSQL e a escolha adequada de banco conforme o tipo de aplicação e os requisitos de desempenho, consistência e escalabilidade.

## Conclusão

O projeto representa uma solução prática para análise de dados de Fórmula 1 em dashboard web, combinando integração com APIs públicas, banco de dados NoSQL e visualização interativa em Python. A parte de Redis e Riak reforça a base teórica e prática sobre diferentes modelos de banco de dados NoSQL, enriquecendo a atividade acadêmica e a visão geral do desenvolvimento do sistema.
