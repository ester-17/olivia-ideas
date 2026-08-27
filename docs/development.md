# Development

## Sobre o desenvolvimento

O OlivIA Ideas começou como um projeto experimental para explorar o uso de Inteligência Artificial na estruturação de ideias.

Com o avanço do desenvolvimento, o foco passou também para a construção de uma base de software mais organizada e sustentável.

A arquitetura foi gradualmente reorganizada para separar:

```text
Interface
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
Database
```

Essa evolução permitiu aplicar na prática conceitos de:

- Programação Orientada a Objetos;
- MVC;
- separação de responsabilidades;
- arquitetura em camadas;
- persistência de dados;
- validação;
- tratamento de exceções;
- integração com serviços externos;
- modelagem de banco de dados.

O projeto continua em desenvolvimento e novas funcionalidades serão adicionadas progressivamente através dos próximos commits.


## Programação Orientada a Objetos

A reorganização do projeto também introduziu uma abordagem orientada a objetos para representar responsabilidades específicas da aplicação.

Entre os principais componentes estão:

- `IdeaService`
- `ValidationService`
- `AIService`
- `AIResponseParser`
- `IdeaRepository`
- `DatabaseConnection`
- `CreateIdeaController`

A utilização de classes permite separar responsabilidades, facilitar a manutenção e preparar o projeto para a expansão do CRUD e das funcionalidades de IA.

Também foram criadas exceções específicas para diferentes camadas, como:

- `ValidationError`
- `DatabaseConnectionError`
- `IdeaRepositoryError`
- `AIServiceError`
- `AIResponseParserError`