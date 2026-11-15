export interface User { id:number; nome:string; email:string; criado_em:string }
export interface Project { id:number; usuario_id:number; nome:string; descricao:string|null; criado_em:string }
export interface Backlog { id:number; projeto_id:number; nome:string; criado_em:string; total_historias:number }
export interface Sprint { id:number; projeto_id:number; nome:string; objetivo:string|null; data_inicio:string|null; data_fim:string|null; criado_em:string; total_historias:number }
export interface Epic { id:number; projeto_id:number; nome:string; descricao:string|null; criado_em:string; total_historias:number }
export interface Criterion { id:number; historia_usuario_id:number; dado:string; quando:string; entao:string; criado_em:string }
export interface Story { id:number; product_backlog_id:number; sprint_backlog_id:number|null; epico_id:number|null; papel:string; acao:string; beneficio:string;
  story_points:number|null; moscow:string|null; rice_reach:number|null; rice_impact:number|null; rice_confidence:number|null; rice_effort:number|null; status:string;
  criado_em:string; texto:string; rice_score:string|null; rice_estado:string; epico_nome:string|null; sprint_nome:string|null; criterios:Criterion[] }
export type StoryForm = Pick<Story, 'papel'|'acao'|'beneficio'|'story_points'|'moscow'|'rice_reach'|'rice_impact'|'rice_confidence'|'rice_effort'|'sprint_backlog_id'|'epico_id'|'status'>
