# Matriz de rastreabilidade — requisitos numerados (1) a (19)

**Base:** Artefatos 2, 3, 4, 5, 6 e 7 revisados. Os códigos `HU-xx` referem-se à versão corrigida do Artefato 4. Os endpoints listados usam o prefixo `/api/v1`. A coluna de teste aponta para funções ou cenários existentes, mas a conformidade no PostgreSQL e no navegador deverá ser homologada em Windows.

| Req. | Comportamento obrigatório | HU | Wireframe | Endpoints principais | Testes relevantes |
|---|---|---|---|---|---|
| (1) | Interface para acesso aos serviços | HU-05 | T01–T10 | Rotas API de todos os módulos | Checklist visual manual |
| (2) | Cadastro, login e logout | HU-01–03 | T01, T02 | `POST /auth/register`, `/auth/login`, `/auth/logout` | `test_auth_cookies_logout_and_csrf` |
| (3) | Serviços privados exigem autenticação | HU-04 | Todas privadas | Dependência `protected` | `test_auth_cookies_logout_and_csrf` |
| (4) | CRUD de projetos | HU-06–09 | T03, T04 | `/projects`, `/projects/{id}` | `test_project_crud_and_user_isolation` |
| (5) | CRUD de Product Backlog; máximo 1/projeto | HU-10–13 | T06 | `/projects/{id}/product-backlog` | `test_pb_uniqueness_and_story_requires_backlog` |
| (6) | CRUD de Sprint Backlogs; múltiplos/projeto | HU-14–17 | T07 | `/projects/{id}/sprints` | `test_full_crud_product_backlog_sprints_epics_and_stories` |
| (7) | CRUD de histórias associadas ao Product Backlog | HU-18–21 | T06, T09 | `/projects/{id}/stories` | `test_full_crud_product_backlog_sprints_epics_and_stories` |
| (8) | Movimentar histórias entre backlogs do mesmo projeto | HU-22 | T06, T07, T09 | `POST /projects/{id}/stories/{story}/move` | `test_sprints_epics_story_criteria_movement_and_cascades`, `test_cross_project_blocked` |
| (9) | Formato Como / Eu quero / Para | HU-18, HU-20 | T09 | `POST/PATCH .../stories` | `test_sprints_epics_story_criteria_movement_and_cascades` |
| (10) | CRUD de épicos | HU-23–26 | T08 | `/projects/{id}/epics` | `test_full_crud_product_backlog_sprints_epics_and_stories` |
| (11) | Vincular história a épico | HU-27 | T08, T09 | `POST/PATCH .../stories` | `test_cross_project_blocked`, `test_sprints_epics_story_criteria_movement_and_cascades` |
| (12) | CRUD de critérios de aceitação | HU-28–31 | T10 | `.../stories/{story}/criteria` | `test_sprints_epics_story_criteria_movement_and_cascades` |
| (13) | Formato Dado / Quando / Então | HU-28, HU-30 | T10 | `POST/PATCH .../criteria` | `test_sprints_epics_story_criteria_movement_and_cascades` |
| (14) | Atribuição de pontos de história | HU-32 | T09 | `POST/PATCH .../stories` | `test_validations_rice_zero_and_not_persisted` |
| (15) | Escala pontos: 0,1,2,3,5,8,13,21,34,55 | HU-32 | T09 | `POST/PATCH .../stories` | `test_validations_rice_zero_and_not_persisted`, `test_integrity_constraints_on_db` |
| (16) | MoSCoW M, S, C, W | HU-33 | T09 | `POST/PATCH .../stories` | `test_validations_rice_zero_and_not_persisted` |
| (17) | Definir RICE | HU-34 | T09 | `POST/PATCH .../stories` | `test_validations_rice_zero_and_not_persisted` |
| (18) | Valores válidos Reach, Impact, Confidence, Effort | HU-34 | T09 | `POST/PATCH .../stories` | `test_validations_rice_zero_and_not_persisted` |
| (19) | Score RICE = (R×I×C)/E | HU-35 | T09 | `.../stories`, `.../stories/{story}` | `test_validations_rice_zero_and_not_persisted` |

## Como verificar integração real

1. Abrir o banco PostgreSQL com pgAdmin e consultar `SELECT id, papel, acao, product_backlog_id, sprint_backlog_id FROM historia_usuario ORDER BY id DESC;`.
2. Salvar uma história pelo React; verificar o registro na tabela.
3. Alterar os campos de uma história; consultar a API e a tabela novamente.
4. Adicionar um critério; conferir sua FK `historia_usuario_id`.
5. Mover a história para uma sprint; confirmar que `sprint_backlog_id` mudou e `product_backlog_id` permaneceu.
6. Excluir uma sprint; confirmar que a história foi preservada com `sprint_backlog_id=NULL`.
7. Verificar que a coluna `rice_score` não existe; o valor é calculado ao consultar a API.

**Nota:** esse checklist de homologação no PostgreSQL deve ser executado pelo grupo no ambiente final. Não há comprovação desse ensaio no ambiente em que o pacote foi gerado.
