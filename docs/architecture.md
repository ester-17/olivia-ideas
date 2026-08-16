# Architecture

```text
┌─────────────────────────────┐
│          Streamlit          │
│    Camada de Apresentação   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Controllers         │
│     Controle do fluxo       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│           Services          │
│       Regras de negócio     │
│       Validação / IA        │
└───────┬─────────────┬───────┘
        │             │
        ▼             ▼
┌──────────────┐ ┌──────────────┐
│ Repositories │ │  AI Service  │
│  Persistência│ │    Gemini    │
└───────┬──────┘ └──────────────┘
        │
        ▼
┌─────────────────────────────┐
│            MySQL            │
└─────────────────────────────┘
```

## 🔄 Fluxo de criação de uma ideia

O fluxo atual de criação segue aproximadamente esta sequência:

```text
Usuário
   │
   ▼
Streamlit
   │
   ▼
CreateIdeaController
   │
   ▼
IdeaService
   │
   ├──► ValidationService
   │
   ▼
IdeaRepository
   │
   ▼
MySQL
```

Quando a IA estiver habilitada no fluxo:

```text
IdeaService
   │
   ├──► AIService
   │       │
   │       ├──► PromptService
   │       │
   │       └──► Gemini API
   │
   ├──► AIResponseParser
   │
   └──► IdeaRepository
             │
             ▼
           MySQL
```

Essa separação permite que a lógica da IA não fique diretamente acoplada à interface.


## Responsabilidades das camadas

### Presentation / Streamlit

Responsável pela interface e pela interação com o usuário.

### Controllers

Recebem os dados da camada de apresentação e delegam a execução para os Services.

Exemplo:

```text
CreateIdeaController
```

### Services

Concentram regras de negócio e orquestram o fluxo da aplicação.

Exemplos:

```text
IdeaService
ValidationService
AIService
AIResponseParser
PromptService
PDFService
```

### Repositories

Responsáveis pela persistência e comunicação com o banco de dados.

Exemplos:

```text
IdeaRepository
UserRepository
AIRepository
```


## Estrutura de pastas 
```text
OlivIA Ideas/
│
├── backend/
│   ├── controllers/
│   │   ├── chat_idea_controller.py
│   │   ├── create_idea_controller.py
│   │   ├── edit_idea_controller.py
│   │   └── list_idea_controller.py
│   │
│   ├── services/
│   │   ├── ai_response_parser.py
│   │   ├── ai_service.py
│   │   ├── idea_service.py
│   │   ├── pdf_service.py
│   │   ├── prompt_service.py
│   │   ├── validation_service.py
│   │   └── prompts/
│   │
│   ├── repositories/
│   │   ├── ai_repository.py
│   │   ├── idea_repository.py
│   │   └── user_repository.py
│   │
│   ├── models/
│   │   ├── analysis.py
│   │   ├── idea.py
│   │   └── user.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── schema.sql
│   │   └── test.sql
│   │
│   └── utils/
│       ├── exceptions.py
│       ├── helpers.py
│       └── logger.py
│
├── frontend/
│   └── pages/
│       ├── chat.py
│       ├── create.py
│       ├── documentation.py
│       ├── edit.py
│       ├── help.py
│       ├── hero.py
│       └── list.py
│
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

> Algumas partes da estrutura já estão preparadas para funcionalidades que ainda serão implementadas nas próximas etapas.

---