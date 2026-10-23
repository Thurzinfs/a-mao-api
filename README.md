# À Mão - Pergunte aos seus documentos

API de assistente pessoal que responde perguntas com base nos **seus próprios arquivos**. O usuário envia PDFs e textos, escolhe quais deseja consultar e recebe respostas com as **fontes** (documento e página).

![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)
![FastAPI](https://img.shields.io/badge/fastapi-async-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

---

## Sumário

- [Sobre](#sobre)
- [Como funciona](#como-funciona)
- [Stack](#stack)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Endpoints](#endpoints)
- [Instalação](#instalação)
- [Variáveis de ambiente](#variáveis-de-ambiente)
- [Privacidade](#privacidade)
- [Roadmap](#roadmap)
- [Licença e contato](#licença-e-contato)

---

## Sobre

O À Mão permite que qualquer pessoa tenha um assistente de busca sobre o que ela mesma guardou: apostilas, manuais, contratos, artigos, anotações. O diferencial é o **escopo**: a cada pergunta, o usuário escolhe se o assistente deve consultar um arquivo, um conjunto de arquivos ou tudo.

O projeto usa **RAG** (Retrieval-Augmented Generation): em vez de enviar documentos inteiros ao modelo, a API busca apenas os trechos relevantes e os entrega à IA para redigir a resposta.

Este repositório contém a **API**. O aplicativo mobile e o site consomem os endpoints abaixo.

---

## Como funciona

**Indexação (ao enviar um arquivo)**

1. O texto é extraído do arquivo (PyMuPDF; OCR para páginas escaneadas).
2. O texto é dividido em trechos (chunks) com sobreposição.
3. Cada trecho vira um vetor (embedding) e é salvo no banco vetorial, junto com metadados: usuário, documento e página.

**Consulta (a cada pergunta)**

1. A pergunta vira um vetor.
2. O banco devolve os trechos mais parecidos, **filtrados pelos documentos escolhidos**.
3. Os trechos entram no prompt do modelo de linguagem.
4. A API responde com o texto gerado e a lista de fontes.

```
Pergunta + escopo ─► Embedding ─► Banco vetorial (filtro) ─► Trechos ─► LLM ─► Resposta + fontes
```

---

## Stack

| Categoria | Tecnologia | Propósito |
|---|---|---|
| API | FastAPI | Endpoints REST assíncronos |
| Extração de texto | PyMuPDF | Leitura de PDFs |
| Embeddings | Sentence Transformers | Vetorização dos trechos |
| Banco vetorial | ChromaDB | Busca por similaridade com filtros |
| LLM | Ollama (local) ou API externa | Geração das respostas |
| Validação | Pydantic | Schemas de entrada e saída |
| Pacotes | uv | Ambiente e lockfile |

> **Requisito:** Python ≥ 3.12

---

## Estrutura do projeto

```
app
├── api
│   ├── dependencies/
│   ├── handlers/
│   └── schemas/
├── application
│   ├── dtos/
│   └── use_cases/
├── domain
│   ├── contracts/
│   ├── entities/
│   ├── exceptions/
│   └── value_objects/
└── infrastructure
    ├── adapters/
    ├── clients/
    ├── database
    │   ├── repositorys/
    │   ├── services/
    │   └── sqlite
    │       ├── database.py
    ├── models/
    └── security/
```

> A estrutura pode mudar conforme o projeto evolui.

---

## Endpoints

**Base URL:** `/api/v1` · **Documentação interativa:** `/docs`

| Método | Rota | Descrição |
|---|---|---|
| POST | `/documentos` | Envia um arquivo e inicia a indexação |
| GET | `/documentos` | Lista os documentos do usuário e seu status |
| DELETE | `/documentos/{id}` | Remove o arquivo e seus vetores |
| POST | `/perguntar` | Faz uma pergunta sobre um ou mais documentos |

### Exemplo: `POST /perguntar`

```json
// Request
{
  "pergunta": "Quantos integrantes pode ter uma equipe?",
  "documentos_ids": ["a1b2c3", "d4e5f6"]
}

// Response 200
{
  "resposta": "As equipes têm de 2 a 4 estudantes, mais um professor ou técnico.",
  "fontes": [
    { "documento": "manual-de-regras.pdf", "pagina": 55 }
  ]
}
```

`documentos_ids` vazio significa "todos os documentos do usuário".

---

## Instalação

**Pré-requisitos**

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Ollama](https://ollama.com/) com um modelo baixado (ex.: `ollama pull qwen2.5:3b`), ou uma chave de API de LLM

```bash
git clone https://github.com/Thurzinfs/a-mao-api.git
cd a-mao-api

cp .env.example .env
uv sync
uv run uvicorn main:app --reload
```

Documentação em `http://localhost:8000/docs`.

---

## Variáveis de ambiente

```bash
# App
SECRET_KEY=sua-chave-secreta

# Armazenamento
UPLOADS_DIR=./uploads
VECTOR_DB_PATH=./index

# Embeddings
EMBEDDING_MODEL=paraphrase-multilingual-MiniLM-L12-v2

# LLM
LLM_MODEL=qwen2.5:3b
OLLAMA_HOST=http://localhost:11434
```

---

## Privacidade

- Cada usuário só acessa os próprios documentos: o filtro por usuário é aplicado **no servidor**, nunca pelo cliente.
- Ao excluir um documento, o arquivo e os vetores associados são removidos.
- Ao usar uma API de LLM externa, os trechos consultados são enviados ao provedor. Com Ollama, tudo permanece na sua máquina.

---

## Roadmap

**Fase 1 · Núcleo RAG**
- [ ] Extração de texto de PDFs
- [ ] Indexação com embeddings e ChromaDB
- [ ] Busca com filtro por arquivo e categoria
- [ ] Geração de respostas com Ollama
- [ ] Descarte de trechos lixo e sobreposição de chunks

**Fase 2 · API**
- [ ] Endpoints de documentos e perguntas
- [ ] Indexação em segundo plano com status
- [ ] Isolamento por usuário

**Fase 3 · Produto**
- [ ] Autenticação
- [ ] Suporte a TXT, DOCX e outros formatos
- [ ] OCR para PDFs escaneados
- [ ] Histórico de conversa e streaming de respostas

**Futuro**
- [ ] Busca híbrida (palavra-chave + vetor) e reranking
- [ ] Banco vetorial de produção (Qdrant ou pgvector)
- [ ] Aplicativo mobile e site

---

## Licença

Este projeto está sob a licença **MIT**.


---

## Contato

- **Autor** — Arthur França Silva
- **E-mail** — arthurfranca.dev@gmail.com
- **GitHub** — [@Thurzinfs](https://github.com/Thurzinfs)

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/Thurzinfs">Arthur França Silva</a>
</div>