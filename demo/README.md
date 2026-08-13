# 💡 IdeaForge AI 

Plataforma inteligente que utiliza IA para transformar ideias iniciais em projetos estruturados, auxiliando na validação e tomada de decisão.

## 🔗 Demo online
Acesse em: https://hjpxjhq3af6tpeg3cjcyfe.streamlit.app/

## 📌 Sobre o projeto
O projeto nasceu da necessidade de resolver um problema comum entre estudantes, desenvolvedores e empreendedores:

> ter boas ideias, mas não saber como validá-las, estruturá-las ou decidir se vale a pena investir.

A proposta é permitir que o usuário insira uma ideia e receba uma análise estruturada com apoio de IA.

---

## 💡 Problema resolvido
Muitas pessoas têm ideias para soluções digitais, mas enfrentam dificuldades como:

- estruturar a ideia
- validar o mercado
- definir o público-alvo
- identificar próximos passos

---

## ⚙️ Funcionalidades (MVP)

- entrada de ideia pelo usuário
- análise inicial com IA
- definição de público-alvo
- estruturação com 5W2H
- sugestão de próximos passos

---

## 🧪 Status do projeto
🚧 **MVP funcional em desenvolvimento**

Este projeto foi desenvolvido inicialmente para fins acadêmicos e portfólio, com foco em aprendizado e experimentação.


---

## 🛠️ Tecnologias utilizadas
- Python
- Streamlit
- Google Generative AI (Gemini API)
- Git / GitHub

---

## ▶️ Como rodar localmente

### 1. Clone o repostiório
    git clone https://github.com/ester-17/idea-forge-ai.git

    cd idea-forge-ai

---

### 2. Crie um ambiente virtual
    python -m venv venv

Ative o ambiente:

Windows:

    venv/Scripts/activate

Linux/MacOS:

    source venv/bin/activate

---
### 3. Instale as dependências
    pip install -r requirements.txt

---

### 4. Configure a API Key

Você pode configurar de duas formas:

#### 🔐 Opção 1 — Variável de ambiente (recomendado)

Windows:

    set GEMINI_API_KEY = sua_chave

Linux/MacOS:

    export GEMINI_API_KEY = sua_chave

####  🔐 Opção 2 — Arquivo .env (local)

Crie o arquivo:

    .env

Conteúdo:

    GEMINI_API_KEY = sua_chave


####  🔐 Opção 3 — Streamlit secrets

Crie o arquivo:

    .streamlit/secrets.toml

Conteúdo:

    GEMINI_API_KEY = "sua_chave"

---

### 5. Execute o projeto
    streamlit run app/app.py

> ⚠️ É necessário possuir uma API Key válida para utilizar a funcionalidade de análise.

---

## 🔄 Roadmap

O roadmap abaixo representa a evolução planejada do produto, priorizando valor para o usuário e escalabilidade.

### v1 - MVP Atual
 
* interface básica com streamlit
* análise inicial de ideias com IA

### v2 - Melhor experiência do usuário

* respostas mais estruturadas
* tratamento de erros
* melhorias na interface

### v3 - Funcionalidades principais

* histórico de ideias
* autenticação de usuários
* dashboards de análises

### v4 - Inteligência de produto

* análise de mercado automatizada
* pontos fortes e fracos de concorrentes
* sugestões estratégicas com IA

---

## 📈 Visão futura
Evoluir o projeto para uma plataforma completa de apoio à criação de produtos digitais, incluindo:

* validação de ideias
* análise de mercado
* geração de MVP
* suporte à tomada de decisão

---

## 👩‍💻 Observação
Este projeto representa um **protótipo funcional inicial (MVP)** em constante contínua, com foco em aprendizado, boas práticas de desenvolvimento e construção de produto.

---