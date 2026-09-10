# 💡 OlivIA Ideas

Plataforma para **organização, estruturação e análise de ideias**, desenvolvida com Python e preparada para utilizar Inteligência Artificial como apoio ao processo de transformação de uma ideia inicial em um projeto mais estruturado.

O projeto começou como o **IdeaForge AI**, um MVP desenvolvido principalmente para explorar a integração entre Streamlit e IA. Com sua evolução, passou por uma reestruturação significativa de arquitetura, organização do código e persistência de dados, dando origem ao **OlivIA Ideas**.

> 🚧 **Status: em desenvolvimento**

> A versão atual está focada na construção da base da aplicação. O fluxo de criação de ideias sem IA está implementado e integrado ao MySQL. A camada de IA já está estruturada no projeto, mas sua integração ainda está em processo de implementação e validação nesta versão.

> 🔗 **Demo online — IdeaForge AI**
>
> Acesse: https://olivia-ideas-demo-f7phr9pugbhhdqlnwanuot.streamlit.app/

---

<details>
<summary>📑 <strong>Sumário</strong></summary>

* [📌 Sobre](#-sobre)
* [Funcionalidades](#-funcionalidades)

  * [Implementado](#implementado)
  * [Em implementação / validação](#em-implementação--validação)
* [Arquitetura](#️-arquitetura)
* [Tecnologias](#️-tecnologias)
* [Como executar](#️-como-executar)
* [Roadmap](#️-roadmap)
* [Explorações futuras](#-explorações-futuras)
* [Visão futura](#-visão-futura)
* [Documentação](#-documentação)
* [Projeto](#-projeto)

</details>

---

## 📌 Sobre

O OlivIA Ideas surgiu a partir de um problema comum entre estudantes, desenvolvedores e empreendedores:

> ter uma boa ideia, mas não saber como organizá-la, estruturá-la ou avaliar seus próximos passos.

A proposta do projeto é oferecer um ambiente onde o usuário possa registrar uma ideia e estruturá-la utilizando a metodologia **5W2H**, com possibilidade de futuramente utilizar IA para auxiliar no preenchimento, refinamento e análise dessas informações.

Além da funcionalidade do produto, o projeto também é utilizado como laboratório para aplicação prática de conceitos de **Engenharia de Software, Programação Orientada a Objetos, arquitetura de aplicações, persistência de dados e integração com serviços de IA**.

---

<details>
<summary><strong>Funcionalidades</strong></summary>

### Implementado

* Interface inicial utilizando Streamlit.
* Criação de ideias.
* Estruturação de ideias com 5W2H.
* Validação do payload e dos campos recebidos.
* Persistência de ideias e dados 5W2H no MySQL.
* Gerenciamento de conexão, commit e rollback do banco.
* Arquitetura organizada em Controllers, Services e Repositories.
* Classes e responsabilidades separadas utilizando Programação Orientada a Objetos.
* Camada específica para comunicação com a API do Gemini.
* Parser para validação e transformação das respostas da IA.
* Tratamento de exceções específicas em diferentes camadas.
* Configuração de credenciais por variáveis de ambiente.

### Em implementação / validação

* Integração completa da IA ao fluxo de criação.
* Geração e refinamento de título com IA.
* Preenchimento e refinamento dos campos do 5W2H com IA.
* Geração e persistência das análises realizadas pela IA.
* Exibição do relatório gerado pela IA.

</details>

---

<details>
<summary><strong>Arquitetura</strong></summary>

A aplicação foi reorganizada para separar a interface, o controle do fluxo, as regras de negócio e o acesso aos dados.

A estrutura atual utiliza uma arquitetura em camadas baseada em **MVC**, com Services e Repositories para separar responsabilidades.

[📐 Acesse a arquitetura aqui](docs/architecture.md)

### Estrutura do projeto

```text
olivia-ideas/
│
├── app/
│   └── app.py
│
├── frontend/
│   └── pages/
│
├── backend/
│   ├── controllers/
│   ├── services/
│   ├── repositories/
│   ├── database/
│   └── ...
│
├── docs/
│   ├── architecture.md
│   └── database/
│
├── requirements.txt
└── README.md
```

</details>

---

<details>
<summary><strong>Tecnologias</strong></summary>

### Linguagem

* Python

### Interface

* Streamlit

### Banco de dados

* MySQL
* MySQL Connector/Python

### Inteligência Artificial

* Google Gemini API
* `google-genai`

### Arquitetura e desenvolvimento

* Programação Orientada a Objetos (POO)
* MVC
* Service Layer
* Repository Pattern
* Validação de dados
* Tratamento de exceções
* Variáveis de ambiente

### Ferramentas

* Git
* GitHub
* python-dotenv

</details>

---

<details>
<summary><strong>Como executar</strong></summary>

### 1. Clone o repositório

```bash
git clone https://github.com/ester-17/olivia-ideas.git
cd olivia-ideas
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente:

**Windows:**

```bash
venv/Scripts/activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

É necessário possuir uma instalação do **MySQL** disponível localmente.

Crie o banco de dados e execute o script:

```text
backend/database/schema.sql
```

Configure as credenciais no arquivo `.env`.

Exemplo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=olivia_ideas
```

### 5. Configure a API Key

A integração com IA ainda está em processo de validação nesta versão.

Você pode configurar de três formas:

#### 🔐 Opção 1 — Variável de ambiente (recomendado)

**Windows:**

```bash
set GEMINI_API_KEY=sua_chave
```

**Linux/macOS:**

```bash
export GEMINI_API_KEY=sua_chave
```

#### 🔐 Opção 2 — Arquivo `.env` (local)

Crie o arquivo:

```text
.env
```

Conteúdo:

```env
GEMINI_API_KEY=sua_chave
```

#### 🔐 Opção 3 — Streamlit Secrets

Crie o arquivo:

```text
.streamlit/secrets.toml
```

Conteúdo:

```toml
GEMINI_API_KEY="sua_chave"
```

### 6. Execute o projeto

Na raiz do projeto:

```bash
streamlit run app/app.py
```

> ⚠️ É necessário possuir uma API Key válida para utilizar as funcionalidades com IA.

</details>

---

<details>
<summary><strong>Roadmap</strong></summary>

### Fase 1 — Fundação

* [x] Protótipo inicial em Streamlit
* [x] Renomeação do projeto para OlivIA Ideas
* [x] Reorganização da arquitetura
* [x] Implementação de POO
* [x] Arquitetura baseada em MVC
* [x] Separação em Controllers, Services e Repositories
* [x] Serviço de validação
* [x] Camada de persistência
* [x] Integração com MySQL
* [x] Criação de ideias sem IA

### Fase 2 — CRUD

* [x] Estrutura inicial para Create
* [ ] Read
* [ ] Update
* [ ] Delete
* [ ] Testes dos fluxos CRUD

### Fase 3 — Inteligência Artificial

* [x] Estrutura do `AIService`
* [x] Integração com Gemini API
* [x] `AIResponseParser`
* [x] Estrutura de prompts
* [ ] Validar integração completa no fluxo atual
* [ ] Geração de título
* [ ] Refinamento do 5W2H
* [ ] Geração de análise completa
* [ ] Persistência das análises

### Fase 4 — Usuários

* [ ] Cadastro
* [ ] Login
* [ ] Autenticação
* [ ] Associação das ideias aos usuários
* [ ] Controle de acesso

### Fase 5 — Evolução da aplicação

* [ ] Melhorias na interface Streamlit
* [ ] Testes automatizados
* [ ] API com FastAPI
* [ ] Frontend com React
* [ ] Melhorias de UX/UI

### Fase 6 — Produto

* [ ] Deploy da aplicação
* [ ] Monitoramento
* [ ] Melhorias de segurança
* [ ] Escalabilidade
* [ ] Funcionalidades avançadas de IA

</details>

---

<details>
<summary><strong>Explorações futuras</strong></summary>

* [ ] Chat contextual sobre uma ideia
* [ ] Análise de mercado
* [ ] Análise de concorrentes
* [ ] Sugestões estratégicas
* [ ] Recursos adicionais de apoio à validação de ideias

</details>

---

## Visão futura

A longo prazo, o objetivo é evoluir o OlivIA Ideas de um protótipo desenvolvido em Streamlit para uma aplicação web completa.

A evolução planejada é:

```text
Protótipo Streamlit
        ↓
Arquitetura estruturada
        ↓
CRUD completo
        ↓
Autenticação
        ↓
Integração completa com IA
        ↓
FastAPI + React
        ↓
Deploy
        ↓
Produto real
```

A ideia é utilizar o projeto não apenas como uma demonstração de integração com IA, mas como uma aplicação completa capaz de evoluir em arquitetura, experiência do usuário e funcionalidades.

---

## Documentação

[📖 Acesse a documentação completa](docs/)

---

## Projeto

**OlivIA Ideas**

Desenvolvido por **Ester Santos Oliveira** como projeto de estudo, portfólio e evolução prática em desenvolvimento de software.
