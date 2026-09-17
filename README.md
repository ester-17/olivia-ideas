# OlivIA Ideas

OlivIA Ideas é uma aplicação de portfólio voltada a estruturação, persistência e análise de ideias de produto. A aplicação combina metodologia 5W2H, Streamlit, MySQL e Google Gemini em um fluxo de criação com contratos explícitos entre interface, regras de negócio e persistência.

O projeto evoluiu do experimento IdeaForge AI para uma aplicação em camadas, com foco em decisões técnicas rastreáveis e evolução sustentável.

## Funcionalidades atuais

- Criação de ideias com título, descrição e 5W2H.
- Preenchimento, geração e refinamento de conteúdo com Gemini.
- Exibição dos dados da ideia e do 5W2H no relatório.
- Análise de negócio por IA: problema, viabilidade, público, riscos, concorrentes e próximos passos.
- Persistência de ideias, 5W2H e análises no MySQL.
- Preservação da origem dos conteúdos (`USER` ou `AI`)

## Demonstração

A versão pública do demo apresenta o conceito de análise de ideias com apoio do Gemini, sem dependência do banco de dados.

**[Demo online](https://olivia-ideas-demo-f7phr9pugbhhdqlnwanuot.streamlit.app/)**

[Documentação do fluxo Create + IA](docs/demo.md)

## Detalhes técnicos
- Arquitetura em camadas com MVC, Service Layer e Repository Pattern.
- Validação de payload e respostas da IA.
- Logging estruturado.
- Configuração segura de credenciais por variáveis de ambiente.

O fluxo atual de desenvolvimento concentra-se na criação e análise de ideias, integrando persistência em MySQL e permitindo combinar dados fornecidos pelo usuário com conteúdo gerado ou refinado pela IA. Leitura, edição, exclusão, autenticação e testes automatizados fazem parte da evolução planejada.

## Arquitetura

O projeto aplica uma arquitetura MVC adaptada para Streamlit, com Service Layer e Repository Pattern:

```text
Streamlit (View) → Controller → Services → Repository → MySQL
                                  └──────→ Gemini API
```

Consulte:
- [Arquitetura](docs/architecture.md)
- [Banco de dados](docs/database.md)
- [Decisões de desenvolvimento](docs/development.md)
- [Demonstração do fluxo Create + AI](docs/demo.md)

## Tecnologias

- Python 3.10+
- Streamlit
- MySQL e MySQL Connector/Python
- Google GenAI SDK (`google-genai`) e Gemini
- `python-dotenv`

## Execução local

```bash
git clone https://github.com/ester-17/olivia-ideas.git
cd olivia-ideas
python -m venv .venv
```

Ative o ambiente e instale as dependências:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Crie o banco `olivia_ideas` e execute [`backend/database/schema.sql`](backend/database/schema.sql). Copie `.env.example` para `.env`:

```env
GEMINI_API_KEY=sua_chave
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=olivia_ideas
```

Inicie a aplicação:

```bash
streamlit run app.py
```

`GEMINI_API_KEY` é necessária apenas quando uma opção de IA é selecionada. O modo “Salvar apenas” não cria o cliente Gemini. Nunca versione `.env`, `.streamlit/secrets.toml` ou credenciais.

## Estrutura

```text
olivia-ideas/
├── app.py
├── frontend/
│   └── pages/                 # View Streamlit
├── backend/
│   ├── controllers/           # Entrada dos casos de uso
│   ├── services/              # Validação, IA e regras de negócio
│   ├── repositories/          # Persistência SQL
│   ├── database/              # Conexão e schema
│   └── utils/                 # Logging
├── docs/
└── requirements.txt
```

## Convenções

Credenciais são obtidas de variáveis de ambiente e nunca devem aparecer em logs. Commits seguem Conventional Commits, por exemplo: `feat: add idea source mapping` e `fix: validate Gemini response`.
