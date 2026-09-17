# Banco de dados

## Estratégia de modelagem

OlivIA Ideas usa MySQL com modelagem híbrida: entidades com relações previsíveis são relacionais; conteúdo variável de análise por IA é armazenado em JSON.
O schema canônico está em [`backend/database/schema.sql`](../backend/database/schema.sql).

## Modelo relacional

```text
users (1) ──────< ideas (1) ────── (1) idea_5w2h
                    │
                    └────────────< ai_analysis
```

`ideas.user_id` é opcional enquanto autenticação não integra o fluxo ativo. Isso permite criar ideias sem conta e preserva a relação para evolução futura.

## Tabelas

### `users`

Reserva a identidade para autenticação futura: `id`, `user_name`, `email`, `password_hash` e `created_at`.

### `ideas`

Entidade principal com `title`, `description`, `status`, timestamps e futura associação opcional com `users`.

### `idea_5w2h`

Possui relação 1:1 com `ideas` por `idea_id UNIQUE`. Mantém os sete campos 5W2H e sua origem:

| Campo | Valor | Origem |
| --- | --- | --- |
| What | `what` | `what_source` |
| Why | `why` | `why_source` |
| Where | `where_location` | `where_location_source` |
| When | `when_info` | `when_source` |
| Who | `who` | `who_source` |
| How | `how` | `how_source` |
| How much | `how_much` | `how_much_source` |

Cada origem é `ENUM('USER', 'AI')`. `USER` representa conteúdo manual inalterado; `AI` representa conteúdo gerado ou refinado pelo Gemini.
O estado `USER_EDITED_AI` não é usado nesta versão.

### `ai_analysis`

Mantém múltiplas análises por ideia. `score` armazena viabilidade numérica para consultas simples; `analysis_data` guarda conteúdo
estruturado — problema, público, riscos, concorrentes e próximos passos — em JSON.

## Motivo da modelagem híbrida

Título, 5W2H e origem possuem formato estável, integridade referencial e valor para filtros futuros; portanto são relacionais.
A análise pode ganhar seções conforme prompts e produto evoluem. JSON evita migração para cada atributo novo, preservando `score` como campo de consulta direta.

## Persistência e transações

`IdeaRepository.create()` insere `ideas` e `idea_5w2h` em uma transação. Falhas provocam rollback.
`save_analysis()` executa uma transação própria após a criação bem-sucedida.

Antes do insert, o repositório exige que os sete valores de origem existam e pertençam a `{USER, AI}`.
Essa validação complementa o `ENUM` do banco e identifica violações de contrato antes do SQL.

## DER visual

![Diagrama de Entidade Relacionamento](assets/der.png)

<details>
<summary>🔍 Clique para ver a versão simplificada em texto (ASCII)</summary>

```text
┌─────────────────┐
│      users      │
├─────────────────┤
│ PK id           │
│ name            │
│ email           │
│ password_hash   │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         │ N
┌────────▼────────┐
│      ideas      │
├─────────────────┤
│ PK id           │
│ FK user_id      │
│ title           │
│ description     │
│ category        │
│ status          │
│ created_at      │
│ updated_at      │
└───────┬─────┬───┘
        │1    │1
        │     │
        │     │N
        │     ▼
        │ ┌─────────────────────────┐
        │ │       ai_analysis       │
        │ ├─────────────────────────┤
        │ │ PK id                   │
        │ │ FK idea_id              │
        │ │ score                   │
        │ │ analysis_data (JSON)    │
        │ │ created_at              │
        │ └─────────────────────────┘
        │
        │1
        │
        │1
┌───────▼────────────────┐
│       idea_5w2h        │
├────────────────────────┤
│ PK id                  │
│ FK idea_id             │
│                        │
│ what                   │
│ what_source            │
│ why                    │
│ why_source             │
│ where_location         │
│ where_location_source  │
│ when_info              │
│ when_source            │
│ who                    │
│ who_source             │
│ how                    │
│ how_source             │
│ how_much               │
│ how_much_source        │
│ created_at             │
│ updated_at             │
└────────────────────────┘
```
</details>



> **Nota:** O DDL versionado em [`backend/database/schema.sql`](../backend/database/schema.sql) é a fonte de verdade para nomes de colunas, nulidade e ENUMs.
