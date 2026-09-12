# Arquitetura

## Visão geral

OlivIA Ideas usa arquitetura em camadas inspirada em MVC. Streamlit cumpre o papel de View; o controller recebe a intenção da tela; services coordenam regras de negócio e integrações; repositories isolam SQL e transações.

```text
┌──────────────┐    ┌────────────┐    ┌─────────────────────┐
│ Streamlit UI │───▶│ Controller │───▶│    IdeaService      │
└──────────────┘    └────────────┘    └───────┬─────────────┘
                                               │
                         ┌─────────────────────┼────────────────────┐
                         ▼                     ▼                    ▼
                ValidationService        AIService            IdeaRepository
                                              │                    │
                                       PromptService/Parser       MySQL
                                              │
                                           Gemini API
```

Essa separação impede que a interface conheça SQL, que a persistência conheça a API externa e que regras de negócio sejam distribuídas entre telas.

## Fluxo Create + IA

1. `frontend/pages/create.py` coleta título, descrição, opções de IA e dados 5W2H.
2. `build_payload()` converte o estado da tela no contrato de entrada do backend.
3. `CreateIdeaController.create_idea()` delega o caso de uso a `IdeaService`.
4. `ValidationService` valida estrutura, tipos e campos obrigatórios.
5. `IdeaService` resolve tarefas: gerar/refinar título, gerar/refinar 5W2H e analisar.
6. Se necessário, `AIService` monta o prompt, chama Gemini e `AIResponseParser` valida o JSON.
7. O service marca `AI` para campos gerados/refinados e `USER` para valores manuais preservados.
8. `IdeaRepository` persiste ideia e 5W2H na mesma transação; análises são persistidas e podem ser renderizadas em Markdown.

O caminho “Salvar apenas” passa por validação e banco, sem criar um cliente Gemini.

## Responsabilidades por camada

### View — `frontend/pages`

Renderiza a interface, coleta entradas, constrói payload e mostra feedback. Não executa SQL ou integrações externas.

### Controller — `backend/controllers`

É a porta de entrada do caso de uso. `CreateIdeaController` recebe o payload e encaminha a execução, mantendo a UI desacoplada do service.

### Services — `backend/services`

- `ValidationService`: valida contrato e tipos.
- `IdeaService`: orquestra criação e atribui a origem do 5W2H.
- `AIService`: integra Gemini e aplica fallback para erros transitórios.
- `PromptService`: compõe instruções modulares.
- `AIResponseParser`: valida JSON e produz relatório Markdown.

### Repository e banco — `backend/repositories` e `backend/database`

`IdeaRepository` encapsula SQL. `DatabaseConnection` gerencia cursor, commit, rollback e encerramento. Essa camada não decide quando chamar IA.

## Contratos e limites

O payload é a fronteira entre View e backend. Widgets Streamlit não vazam para services: o contrato usa `idea`, `options`, `methodology.data` e `methodology.sources`. Respostas do Gemini são validadas antes de alterar o payload.

Exceções específicas preservam o contexto da falha por camada, e logs estruturados permitem diagnóstico sem registrar segredos.

## Estrutura vigente

```text
backend/
├── controllers/create_idea_controller.py
├── database/{connection.py,schema.sql}
├── repositories/idea_repository.py
├── services/{ai_response_parser.py,ai_service.py,idea_service.py,prompt_service.py,validation_service.py,prompts/}
└── utils/logger.py
frontend/pages/{hero.py,create.py}
```

Leitura, edição, exclusão e autenticação não fazem parte do fluxo ativo; devem ser adicionadas como novos casos de uso.
