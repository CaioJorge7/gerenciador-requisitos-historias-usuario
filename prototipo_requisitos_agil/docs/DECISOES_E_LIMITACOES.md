# Decisões técnicas propostas e limitações

Versões corrigidas dos Artefatos 3–7 e 9 foram consideradas. Não se presume aprovação formal das opções ainda identificadas como propostas nos documentos.

## Propostas implementadas

1. **Frontend:** React + TypeScript + Vite, em português brasileiro, com layout responsivo orientado pelas telas T01–T11.
2. **Backend:** FastAPI, Pydantic e SQLAlchemy; endpoints REST sob `/api/v1`.
3. **Persistência principal:** PostgreSQL, criado por uma revisão Alembic estável e oito tabelas conforme A7. SQLite é usado **apenas pelos testes automatizados**.
4. **Sessão:** identificador opaco aleatório enviado em cookie HttpOnly; tabela `sessao` guarda apenas hash SHA-256; expiração após 30 minutos de inatividade e limite absoluto de oito horas; CSRF por token vinculado à sessão e conferido no servidor.
5. **Backlogs:** a história permanece vinculada ao único Product Backlog; `sprint_backlog_id=NULL` significa não alocada. Alocar/mover uma história altera apenas o ID da sprint.
6. **Épico:** vínculo opcional 0..1 por história. Excluir épico preserva as histórias e aplica `SET NULL`.
7. **Exclusão:** Product Backlog exclui suas histórias e critérios em cascata; excluir sprint devolve as histórias ao catálogo de disponíveis; excluir projeto remove seus dependentes. A interface solicita confirmação.
8. **RICE:** Confidence percentual é convertida para fração; Effort igual a zero retorna estado `NAO_CALCULAVEL`, campos ausentes retornam `PENDENTE`; apenas os parâmetros são persistidos, não o score calculado.
9. **Status:** campo opcional de acompanhamento A_FAZER, EM_ANDAMENTO, CONCLUIDA foi incluído por constar no A7. Não altera os 19 requisitos obrigatórios.

## Limitações conscientemente mantidas

- A autorização por proprietário e a igualdade de projeto entre história, sprint e épico são validadas na camada de **serviço/API**. O modelo físico ainda não tem FKs compostas que reforcem a igualdade do projeto se alguém executar SQL diretamente; as FKs individuais evitam apenas referências inexistentes. Reforço físico poderá ser introduzido numa migração futura.
- O controle de acesso considera um proprietário por projeto. Colaboração/convites (FE-19) e exportação PDF/CSV (FE-20) não foram implementados por serem opcionais.
- Não há rate limiting de login, auditoria avançada, isolamento por tenant no banco, backup automatizado em produção nem MFA. O protótipo não foi homologado como serviço público.
- Os requisitos de desempenho e acessibilidade precisam de aferição no ambiente Windows com PostgreSQL e browsers instalados.
- A interface React depende de `npm install`. Não foi possível instalar os pacotes npm nem executar o build neste ambiente por ausência de acesso à registry. O código TSX foi validado sintaticamente, mas o fluxo navegador/API completo precisa ser conferido localmente.
- O PostgreSQL não estava disponível no ambiente de elaboração. Migração e seed passaram em SQLite temporário e a API passou nos testes automatizados, sem comprovar equivalência de desempenho e operações no PostgreSQL.
- Caso a equipe escolha outra política de exclusão, autenticação ou cardinalidade de épicos, será necessária atualização conjunta dos Artefatos 4–9 e do código.

## Checklist de aprovação da equipe

- [ ] Ratificar a pilha de tecnologias proposta.
- [ ] Ratificar as políticas de exclusão em cascata e SET NULL.
- [ ] Ratificar os estados de RICE e a conversão percentual de Confidence.
- [ ] Ratificar a cardinalidade de épicos (no máximo um por história).
- [ ] Aprovar sessões no servidor e controles de segurança.
- [ ] Executar migração + seed em PostgreSQL no computador de apresentação.
- [ ] Compilar frontend e testar manualmente todas as telas no Chrome/Firefox.
- [ ] Conferir a matriz de rastreabilidade e executar o roteiro de demonstração.
