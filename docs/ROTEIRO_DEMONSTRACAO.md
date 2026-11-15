# Roteiro acadêmico — demonstração do Artefato 8

**Objetivo:** provar os três critérios do professor: (1) aderência ao design; (2) integração real; (3) funcionalidades corretas.

## Preparação

1. Verificar que o PostgreSQL está ativo, que `alembic upgrade head` foi executado e que existe um usuário de demonstração.
2. Iniciar backend e frontend. Abrir http://127.0.0.1:5173 ou a versão compilada servida pelo FastAPI.
3. Deixar o pgAdmin pronto para consultar `usuario`, `projeto`, `product_backlog`, `historia_usuario` e `criterio_aceitacao`.
4. Fechar sessões antigas e verificar que não existem alterações conflitantes entre os dados demonstrativos.
5. Se houver conexão com a internet, não compartilhar a senha de teste fora do ambiente local.

## Fluxo recomendado

| Ordem | Ação na interface | O que demonstrar |
|---:|---|---|
| 1 | Tela de login → cadastro | Validação de nome/e-mail/senha, autenticação verdadeira |
| 2 | Criar projeto | Registro aparece na lista e na tabela `projeto` |
| 3 | Entrar no projeto | Navegação condizente com o storyboard T03–T05 |
| 4 | Criar Product Backlog | Apenas um por projeto, tentativa de segundo deve ser rejeitada |
| 5 | Criar duas sprints | Várias sprints no mesmo projeto, datas consistentes |
| 6 | Criar um épico | Épico vinculado ao projeto |
| 7 | Criar uma história com papel, ação e benefício | Formato estruturado e texto composto automaticamente |
| 8 | Selecionar épico e sprint | Vínculos restritos ao projeto; preservação da história |
| 9 | Atribuir Story Points = 8 e MoSCoW = M | Restrições de listas fechadas |
| 10 | Informar RICE: Reach 200, Impact 2, Confidence 80%, Effort 8 | Score oficial `40,00` obtido da API |
| 11 | Criar critério Dado/Quando/Então | CRUD e FK com a história |
| 12 | Abrir Product Backlog e trocar sprint | Alteração de `sprint_backlog_id`, sem perder `product_backlog_id` |
| 13 | Alterar a história | Mostrar mudança efetiva no PostgreSQL e após atualizar a página |
| 14 | Excluir sprint | História permanece no Product Backlog sem alocação |
| 15 | Excluir épico | História permanece e `epico_id` torna-se NULL |
| 16 | Excluir uma história (com confirmação) | Critérios removidos em cascata e ausência de órfãos |
| 17 | Logout | Tentativa de voltar ao projeto exige login válido |

## Validações negativas importantes

- Cadastrar história sem Product Backlog: erro de negócio.
- Criar segundo Product Backlog no mesmo projeto: `409 Conflict`.
- Pontuação `4` ou `7`: erro `422` na API; seletor não oferece valores inválidos.
- Impact `5` ou Confidence `60%`: erro `422`.
- Effort `0`: score **Não calculável**, sem divisão por zero.
- Vincular história a épico/sprint de outro projeto: `404`, sem alteração.
- Consultar recurso pertencente a outra conta: `404` e sem vazamento de dados.
- Executar POST sem CSRF: `403`.

## Evidências para a apresentação

Abrir DevTools > Network para mostrar a requisição real à API, o status HTTP e os dados JSON; abrir pgAdmin para mostrar o registro. O frontend não possui armazenamento de domínio em localStorage. Valores RICE são derivados e não existe coluna `rice_score` no banco.

**Checklist:** antes de declarar a funcionalidade aprovada, verifique a operação no ambiente real e registre o resultado do teste do grupo.
