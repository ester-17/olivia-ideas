# Desenvolvimento

## 1. Responsabilidade e Fluxo da Página de Criação

O módulo `frontend/pages/create.py` é a fronteira de interação do caso de uso de criação. Ele coleta título, descrição, preferências de geração/refinamento por IA, dados manuais 5W2H e a opção de análise. A tela não contém SQL nem regras de orquestração do Gemini.

`render_form()` produz o estado da interface. `build_payload()` o transforma no contrato de backend. `submit()` delega o contrato a `CreateIdeaController.create_idea()`, que chama `IdeaService`. Ao final, a página mostra sucesso ou erro e renderiza o relatório Markdown quando solicitado.

## 2. Evolução da Implementação e Estimativa de Prazos

A variação entre estimativa inicial e implementação decorreu de evolução de escopo, não de atraso isolado. Persistência transacional, validação de respostas estruturadas, rastreabilidade de origem por campo, logging e padronização arquitetural exigiram decisões não visíveis no protótipo.

Estimativas no desenvolvimento de software representam previsões baseadas no conhecimento inicial, e adequações arquiteturais fazem parte do refinamento técnico da aplicação.

## 3. Gestão de Credenciais e Segurança (Vazamento de API Keys)

No histórico inicial ocorreu a exposição acidental de uma chave da API Gemini. A contenção apropriada inclui revogação ou rotação imediata no provedor, remoção da credencial do código, uso de variáveis de ambiente (`.env`) ou `st.secrets`, atualização do `.gitignore` e verificação de que logs não recebam a chave.

Informações sensíveis e credenciais jamais devem fazer parte do código-fonte ou ser versionadas no repositório.

## 4. Padronização e Convenções Adotadas

O amadurecimento técnico foi organizado em três pilares:

- **Documentação:** docstrings no padrão Google Style para classes e métodos.
- **Código:** nomenclatura PEP 8, `typing.Mapping` para parâmetros somente leitura, type hints rigorosos, separação de responsabilidades (SRP) e remoção de código morto ou `print()` temporário.
- **Git:** adoção do padrão Conventional Commits para rastreabilidade e histórico profissional.

## 5. Observabilidade e Logging

Feedback visual do Streamlit é útil ao usuário, mas não basta para operar ou diagnosticar a aplicação. O fluxo usa logging estruturado com `logger.info`, `logger.warning` e `logger.exception`, permitindo acompanhar execução no terminal e no arquivo rotativo de logs.

Eventos de log não devem conter chaves de API, senhas ou dados sensíveis. O conteúdo registrado deve ser proporcional ao diagnóstico necessário.

## 6. Transformação de Dados e Contrato do Payload

O caminho é `form_data` → `build_payload()` → `payload` → controller. A separação impede que detalhes de widgets Streamlit definam o contrato do domínio. O payload organiza `idea`, `methodology.data`, opções e preferências de IA; o backend acrescenta `methodology.sources` compatível com as chaves de origem `*_source`.

Isso permite adequar nomenclaturas como `where` para `where_location` apenas no mapper SQL, sem acoplar a UI ao schema físico.

## 7. Separação de Responsabilidades (Clean Code / SRP)

A interface segue `configure_page()` → `render_form()` → `build_payload()` → `submit()` → controller. Cada função possui uma intenção isolada: apresentação, coleta, adaptação de dados ou delegação. A decomposição evita uma `main()` monolítica e reduz o risco de alterações de UI no fluxo de negócio.

## 8. Tabela de Problemas, Decisões e Aprendizados

| Problema Encontrado                         | Solução / Decisão Técnica                                                             | Aprendizado de Engenharia                                                  |
| :------------------------------------------ | :------------------------------------------------------------------------------------ | :------------------------------------------------------------------------- |
| Exposição de chave da API                   | Remoção da credencial, rotação no provedor e isolamento em `.env`/`secrets`           | Gestão de segurança de credenciais e uso do `.gitignore` desde a concepção |
| Crescimento da lógica de interface          | Decomposição da página em funções com responsabilidade única                          | Aplicação de Clean Code e Princípio da Responsabilidade Única (SRP)        |
| Dificuldade no diagnóstico de erros         | Substituição de `print()` por logging estruturado com níveis e tratamento de exceções | Importância da observabilidade em produção sem depender de UI              |
| Divergência de contratos entre UI e Backend | Implementação do pipeline de transformação com `build_payload()`                      | Separação clara entre a camada de View e a camada de Controller/Service    |
| Tipagem e imutabilidade de dados            | Uso de `type hints` avançados e `Mapping` para parâmetros somente leitura             | Contratos de interface e prevenção de efeitos colaterais em coleções       |
| Documentação e histórico inconsistentes     | Adoção de docstrings no padrão Google e histórico em Conventional Commits             | Manutenibilidade do código e rastreabilidade profissional no versionamento |
| Variação no tempo de desenvolvimento        | Acomodação de refatorações de arquitetura e ajustes de qualidade                      | Estimativa como previsão e necessidade de considerar débitos técnicos      |
