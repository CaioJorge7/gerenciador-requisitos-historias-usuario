# Relatório dos testes efetivamente executados

Data de elaboração: 14/11/2026. Ambiente: Python 3.13, FastAPI 0.128.2, SQLAlchemy 2.0.50, Alembic 1.18.4, pytest 9.0.2, banco **SQLite temporário para teste**.

## Testes executados

| Teste | Situação | Escopo |
|---|---|---|
| `test_auth_cookies_logout_and_csrf` | APROVADO | Cadastro, duplicação de e-mail, login, CSRF, logout, reutilização de sessão |
| `test_project_crud_and_user_isolation` | APROVADO | CRUD de projeto e isolamento entre contas |
| `test_pb_uniqueness_and_story_requires_backlog` | APROVADO | Máximo um Product Backlog, história depende do backlog |
| `test_sprints_epics_story_criteria_movement_and_cascades` | APROVADO | CRUD parcial, vínculo, movimento, critérios, `ON DELETE SET NULL`, cascata |
| `test_cross_project_blocked` | APROVADO | Bloqueio de sprint/épico em projeto incorreto |
| `test_validations_rice_zero_and_not_persisted` | APROVADO | Domínios fechados, RICE correto, E=0, score não persistido |
| `test_integrity_constraints_on_db` | APROVADO | `UNIQUE`, `CHECK` e `FOREIGN KEY` no banco de teste |
| `test_full_crud_product_backlog_sprints_epics_and_stories` | APROVADO | Atualizações e exclusões dos módulos principais |
| `test_session_idle_expiration_and_cookie_exposure` | APROVADO | Expiração após 30 minutos de inatividade |
| `test_fast_list_500_stories_in_test_environment` | APROVADO | Listagem de 500 histórias em menos de 3 segundos **apenas no SQLite de teste** |

**Resultado:** 10/10 testes automatizados aprovados (pytest).

### Migrações e seed

`alembic upgrade head` executado em banco SQLite vazio de teste, criando oito tabelas e a tabela de versão do Alembic. `seed.py` executado sobre esse mesmo ambiente e inseriu **5 histórias e 5 critérios**. `alembic current` retornou `0001 (head)`.

### Verificação do frontend

Arquivos `.ts` e `.tsx` analisados pelo compilador TypeScript em modo de transpilação isolada: sem erros de sintaxe. **Não houve compilação Vite, typecheck completo nem teste visual de navegador**, pois o registro npm estava inacessível no ambiente de execução da elaboração.

### Pendências para homologação no Windows

- [ ] Instalar dependências `npm install` e executar `npm run build` sem erros.
- [ ] Executar todas as 11 telas com backend e PostgreSQL ativos.
- [ ] Verificar criação, edição, exclusão e efeitos no banco com pgAdmin.
- [ ] Medir o tempo de consulta de 500 histórias no PostgreSQL.
- [ ] Verificar contraste, navegação por teclado e compatibilidade Chrome/Firefox.
- [ ] Testar HTTPS com certificado local válido e `COOKIE_SECURE=true`.

**Nunca apresente estes testes locais como comprovação de aprovação no PostgreSQL final.**
