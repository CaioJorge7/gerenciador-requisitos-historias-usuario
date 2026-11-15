# Requisito. — Protótipo do Sistema de Gerenciamento de Requisitos com Histórias de Usuário

Protótipo acadêmico com frontend **React + TypeScript + Vite** e API **FastAPI + SQLAlchemy + Alembic + PostgreSQL**. Implementa autenticação com sessão no servidor, projetos, Product Backlog, Sprint Backlogs, épicos, histórias, critérios, Story Points, MoSCoW e cálculo RICE.

**Atenção:** esta entrega contém **código-fonte executável** e testes do backend, não uma aplicação já hospedada. Para rodar na sua máquina é necessário instalar Python, Node.js, PostgreSQL e dependências. As telas ainda precisam ser compiladas e verificadas no navegador do seu Windows.

## Início rápido no Windows

### 1. Pré-requisitos

- **Python 3.12**, disponível pelo comando `py -3.12 --version`;
- **Node.js 20 LTS ou 22** e npm (`node --version`);
- **PostgreSQL 16 ou compatível**, instalado localmente (também pode usar pgAdmin);
- Acesso à internet **somente para instalar as dependências**.

### 2. Preparar o banco PostgreSQL

No pgAdmin Query Tool, conecte-se usando uma conta administrativa e execute:

```sql
CREATE USER requisitos WITH PASSWORD 'SENHA_LOCAL_FORTE_AQUI';
CREATE DATABASE requisitos_agil OWNER requisitos;
```

Em algumas versões do pgAdmin, `CREATE DATABASE` precisa ser executado como comando independente. Se o usuário ou o banco já existir, não repita a criação.

### 3. Instalar dependências

Na pasta raiz do projeto, abra o PowerShell:

```powershell
.\scripts\instalar_windows.ps1
```

Se o Windows bloquear a execução de scripts, execute os comandos manualmente em um PowerShell autorizado, sem alterar permanentemente a política do computador.

Configure o arquivo `backend\.env` copiado do modelo `.env.example`, alterando `DATABASE_URL` para a senha escolhida. Gere e configure uma chave aleatória longa para `APP_SECRET_KEY`, por exemplo:

```powershell
py -3.12 -c "import secrets; print(secrets.token_hex(32))"
```

**Jamais envie seu `.env`, senhas ou tokens para um repositório público.**

### 4. Criar tabelas e inserir dados de teste

Abra um PowerShell na pasta `backend`:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe seed.py
```

As migrações criam as **oito tabelas com chaves, índices e restrições**. O seed é idempotente e insere dados apenas se a conta fictícia ainda não existir.

**Conta de demonstração (somente uso local):**

- E-mail: `demo@requisitos.local`
- Senha: `Demo123456!`

A senha está destinada exclusivamente a demonstrar a aplicação em ambiente acadêmico isolado. Não a utilize em ambiente público nem em dados reais.

### 5. Iniciar o backend

Em uma janela de PowerShell na raiz:

```powershell
.\scripts\iniciar_backend.ps1
```

O backend fica disponível em **http://127.0.0.1:8000**. Documentação interativa: **http://127.0.0.1:8000/docs**. Saúde da API: `/api/v1/health`.

### 6. Iniciar o frontend

Em **outra** janela de PowerShell:

```powershell
.\scripts\iniciar_frontend.ps1
```

Abra **http://127.0.0.1:5173** no navegador. O Vite faz proxy das chamadas `/api` para o FastAPI, mantendo cookies no mesmo domínio do navegador.

> Para teste em `localhost`, a configuração é `COOKIE_SECURE=false`; **em HTTPS**, altere para `true`.

### 7. Compilar a aplicação para a apresentação

```powershell
.\scripts\compilar_frontend.ps1
```

O build fica em `frontend\dist`. Ao iniciar o backend depois do build, o FastAPI detecta essa pasta e serve a interface na mesma origem: **http://127.0.0.1:8000** (sem precisar manter o servidor Vite ativo).

Para demonstrar HTTPS no Windows, gere um certificado local confiável conforme instruções do Artefato 9 e inicie o Uvicorn usando `--ssl-certfile` e `--ssl-keyfile`. Com HTTPS verdadeiro, defina `COOKIE_SECURE=true` no `.env` e acesse sempre pelo nome de host correspondente ao certificado.

## Testes automatizados

Na pasta `backend` após instalar dependências:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Os testes automatizados utilizam **SQLite temporário somente nos testes**. Eles exercitam a API, sessões, CSRF, segregação entre contas, integridade, movimentação, cálculo e 500 histórias. **Não substituem a verificação final com PostgreSQL**.

### Resultados verificados no ambiente de elaboração

- **10/10 testes de backend aprovados** com Python 3.13 e dependências disponíveis no ambiente de elaboração;
- Migração Alembic executada e seed carregado com sucesso em SQLite temporário;
- Código TS/TSX analisado pelo parser TypeScript sem erros de sintaxe;
- **Não foi possível instalar dependências npm nem compilar o frontend** devido à indisponibilidade de conexão com o registro npm neste ambiente;
- **Não havia servidor PostgreSQL disponível** para homologação. O desempenho de 500 histórias foi validado somente em SQLite de teste e não atesta a meta no PostgreSQL.

Os resultados são registrados em `docs/RELATORIO_DE_TESTES.md`.

## Funcionalidades implementadas

| Módulo | Funcionalidades |
| --- | --- |
| Acesso | Cadastro, login, logout, sessões armazenadas no banco, CSRF e isolamento entre contas |
| Projetos | Criar, listar, consultar, editar e excluir com confirmação |
| Product Backlog | CRUD, unicidade por projeto, exigência de backlog antes das histórias |
| Sprint Backlogs | CRUD, datas opcionais consistentes, múltiplas sprints, exclusão preserva histórias |
| Épicos | CRUD, máximo um épico por história, exclusão desvincula histórias |
| Histórias | CRUD, campos estruturados, pré-visualização, alocação em sprint e retorno |
| Critérios | CRUD, Dado / Quando / Então, exclusão em cascata com a história |
| Estimativas | Fibonacci modificada, MoSCoW, Reach, Impact, Confidence, Effort e score RICE |
| Dashboard | Listagens e indicadores **consultados na API real** |

**Fora do escopo inicial:** colaboração/convites e exportação de PDF/CSV (funcionalidades opcionais FE-19/FE-20). Filtros simples de interface e status de histórias foram incluídos por já existirem no design e no esquema de referência.

## Arquitetura e organização dos arquivos

```text
prototipo_requisitos_agil/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI, middleware e resposta SPA
│   │   ├── security.py             # Argon2, sessão, cookies e CSRF
│   │   ├── schemas.py              # Contratos de entrada e saída Pydantic
│   │   ├── services.py             # Regras de domínio e cálculo RICE
│   │   ├── repositories.py         # Consultas ORM
│   │   ├── models.py               # 8 tabelas e restrições
│   │   ├── database.py             # Conexão e transações
│   │   └── routers/                # API REST /api/v1
│   ├── alembic/versions/0001_initial.py
│   ├── tests/test_api.py          # Cenários integrados
│   ├── seed.py                     # Dados fictícios de demonstração
│   └── .env.example
├── frontend/
│   ├── src/pages/                # Telas T01–T11
│   ├── src/components/           # Design system
│   ├── src/api.ts                 # Cliente HTTP
│   └── src/styles.css            # Layout responsivo
├── docs/
│   ├── MATRIZ_RASTREABILIDADE.md
│   ├── DECISOES_E_LIMITACOES.md
│   ├── ROTEIRO_DEMONSTRACAO.md
│   └── RELATORIO_DE_TESTES.md
└── scripts/                     # PowerShell / Windows
```

**Fluxo:** React (Apresentação) → FastAPI (Controle) → `services.py` (Negócio) → `repositories.py` (Persistência) → SQLAlchemy/Alembic → PostgreSQL.

## Regras importantes

- O Product Backlog permanece como catálogo mestre. `product_backlog_id` é obrigatório; `sprint_backlog_id` é opcional. Excluir uma sprint aplica `SET NULL` às histórias alocadas. Excluir o Product Backlog remove as histórias e critérios, após confirmação na interface.
- Uma história só pode referenciar uma sprint ou épico do **mesmo projeto**, regra validada no Service. As FKs individuais não bastam para impor essa igualdade no banco (vide decisões e limitações).
- RICE: `(Reach × Impact × Confidence/100) ÷ Effort`, com saída em duas casas decimais. `Effort = 0` → **Não calculável**; campos ausentes → **Pontuação pendente**. O valor derivado não é gravado no banco.
- Uma história pode ter zero ou um épico e zero ou uma sprint.
- As exclusões são efetivamente realizadas pelo banco conforme as ações de chave estrangeira.

## Segurança do protótipo

Senhas com hash Argon2, sessões opacas no servidor (no banco só o hash do identificador), cookies `HttpOnly` para a sessão, `SameSite=Lax`, controle de acesso por proprietário e CSRF obrigatório em ações autenticadas de escrita. Configure `COOKIE_SECURE=true` quando usar HTTPS.

Este é um protótipo acadêmico, **não um produto pronto para exposição pública**. Para produção real, ainda seriam necessários ensaios de segurança adicionais, controle contra tentativas repetidas de login, gerenciamento operacional de segredos, backup, observabilidade e revisão de permissões.

## Materiais para o professor

Consulte `docs/MATRIZ_RASTREABILIDADE.md` e `docs/ROTEIRO_DEMONSTRACAO.md` para demonstrar os três critérios de avaliação: aderência ao design, integração efetiva e correção funcional.
