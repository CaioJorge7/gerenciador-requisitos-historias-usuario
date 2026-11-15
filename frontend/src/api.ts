/** A persistência e as regras de negócio pertencem ao servidor; nunca ao localStorage. */
import type { User, Project, Backlog, Sprint, Epic, Story, Criterion, StoryForm } from './types'

const root = '/api/v1'

function csrfCookie(): string {
  const token = document.cookie.split('; ').find(v => v.startsWith('sr_csrf='))
  return token ? decodeURIComponent(token.split('=').slice(1).join('=')) : ''
}

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message) }
}

export async function request<T>(path: string, method = 'GET', data?: unknown): Promise<T> {
  const headers: Record<string,string> = {}
  if (data !== undefined) headers['Content-Type'] = 'application/json'
  if (!['GET', 'HEAD'].includes(method)) {
    const token = csrfCookie()
    if (token) headers['X-CSRF-Token'] = token
  }
  let response: Response
  try {
    response = await fetch(root + path, { method, headers, credentials: 'include', body: data !== undefined ? JSON.stringify(data) : undefined })
  } catch {
    throw new ApiError(0, 'Não foi possível conectar ao servidor. Verifique se o backend está em execução.')
  }
  if (response.status === 204) return undefined as T
  const json = await response.json().catch(() => ({}))
  if (!response.ok) {
    const detail = json.detail
    const message = typeof detail === 'string' ? detail : Array.isArray(detail)
      ? detail.map((x: { loc?: (string|number)[], msg?: string }) => `${x.loc?.slice(-1)[0] ?? 'Campo'}: ${x.msg ?? 'inválido'}`).join('; ')
      : 'A operação não pôde ser concluída.'
    if (response.status === 401) window.dispatchEvent(new Event('sr:unauthorized'))
    throw new ApiError(response.status, message)
  }
  return json as T
}

export const api = {
  me: () => request<User>('/auth/me'),
  login: (email:string, senha:string) => request<User>('/auth/login','POST',{email,senha}),
  register: (nome:string,email:string,senha:string) => request<User>('/auth/register','POST',{nome,email,senha}),
  logout: () => request<void>('/auth/logout','POST'),
  projects: () => request<Project[]>('/projects'),
  project: (pid:number) => request<Project>(`/projects/${pid}`),
  createProject: (data:{nome:string;descricao:string|null}) => request<Project>('/projects','POST',data),
  editProject: (id:number,data:{nome:string;descricao:string|null}) => request<Project>(`/projects/${id}`,'PATCH',data),
  deleteProject: (id:number) => request<void>(`/projects/${id}`,'DELETE'),
  backlog: (pid:number) => request<Backlog|null>(`/projects/${pid}/product-backlog`),
  createBacklog: (pid:number,nome:string) => request<Backlog>(`/projects/${pid}/product-backlog`,'POST',{nome}),
  editBacklog: (pid:number,nome:string) => request<Backlog>(`/projects/${pid}/product-backlog`,'PATCH',{nome}),
  deleteBacklog: (pid:number) => request<void>(`/projects/${pid}/product-backlog`,'DELETE'),
  sprints: (pid:number) => request<Sprint[]>(`/projects/${pid}/sprints`),
  createSprint: (pid:number,data:unknown) => request<Sprint>(`/projects/${pid}/sprints`,'POST',data),
  editSprint: (pid:number,id:number,data:unknown) => request<Sprint>(`/projects/${pid}/sprints/${id}`,'PATCH',data),
  deleteSprint: (pid:number,id:number) => request<void>(`/projects/${pid}/sprints/${id}`,'DELETE'),
  epics: (pid:number) => request<Epic[]>(`/projects/${pid}/epics`),
  createEpic: (pid:number,data:unknown) => request<Epic>(`/projects/${pid}/epics`,'POST',data),
  editEpic: (pid:number,id:number,data:unknown) => request<Epic>(`/projects/${pid}/epics/${id}`,'PATCH',data),
  deleteEpic: (pid:number,id:number) => request<void>(`/projects/${pid}/epics/${id}`,'DELETE'),
  stories: (pid:number) => request<Story[]>(`/projects/${pid}/stories`),
  story: (pid:number,stid:number) => request<Story>(`/projects/${pid}/stories/${stid}`),
  createStory: (pid:number,data:StoryForm) => request<Story>(`/projects/${pid}/stories`,'POST',data),
  editStory: (pid:number,id:number,data:StoryForm) => request<Story>(`/projects/${pid}/stories/${id}`,'PATCH',data),
  deleteStory: (pid:number,id:number) => request<void>(`/projects/${pid}/stories/${id}`,'DELETE'),
  moveStory: (pid:number,id:number,sprint_backlog_id:number|null) => request<Story>(`/projects/${pid}/stories/${id}/move`,'POST',{sprint_backlog_id}),
  criteria: (pid:number,stid:number) => request<Criterion[]>(`/projects/${pid}/stories/${stid}/criteria`),
  createCriterion: (pid:number,stid:number,data:unknown) => request<Criterion>(`/projects/${pid}/stories/${stid}/criteria`,'POST',data),
  editCriterion: (pid:number,stid:number,cid:number,data:unknown) => request<Criterion>(`/projects/${pid}/stories/${stid}/criteria/${cid}`,'PATCH',data),
  deleteCriterion: (pid:number,stid:number,cid:number) => request<void>(`/projects/${pid}/stories/${stid}/criteria/${cid}`,'DELETE'),
}
