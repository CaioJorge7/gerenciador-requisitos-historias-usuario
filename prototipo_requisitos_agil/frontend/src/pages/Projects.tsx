import type React from 'react'
import {useEffect,useState} from 'react'
import {ArrowRight, FolderOpen, Layers3, MoreHorizontal, Pencil, Plus, Search, Trash2, CalendarDays} from 'lucide-react'
import {useNavigate} from 'react-router-dom'
import {api} from '../api'
import {useToast} from '../contexts'
import type {Project} from '../types'
import {Button,Confirm,Empty,Field,Message,Modal,SectionTitle} from '../components/ui'

export function ProjectsPage(){
  const nav=useNavigate();const {push}=useToast();const [items,setItems]=useState<Project[]>([]);const [query,setQuery]=useState('');const [loading,setLoading]=useState(true)
  const [edit,setEdit]=useState<Project|null|undefined>(undefined);const [remove,setRemove]=useState<Project|null>(null)
  const [nome,setNome]=useState('');const [descricao,setDescricao]=useState('');const [busy,setBusy]=useState(false);const [error,setError]=useState('')
  const load=async()=>setItems(await api.projects())
  useEffect(()=>{load().catch(err=>setError(err.message)).finally(()=>setLoading(false))},[])
  function openEdit(item:Project|null){setEdit(item);setNome(item?.nome||'');setDescricao(item?.descricao||'');setError('')}
  async function save(e:React.FormEvent){e.preventDefault();setBusy(true);setError('');try{if(edit){await api.editProject(edit.id,{nome,descricao})}else{await api.createProject({nome,descricao})}await load();setEdit(undefined);push(edit?'Projeto atualizado com sucesso.':'Projeto criado com sucesso.')}catch(err:any){setError(err.message)}finally{setBusy(false)}}
  async function deleteIt(){if(!remove)return;setBusy(true);try{await api.deleteProject(remove.id);await load();setRemove(null);push('Projeto excluído permanentemente.')}catch(err:any){push(err.message,'error')}finally{setBusy(false)}}
  const filtered=items.filter(x=>`${x.nome} ${x.descricao||''}`.toLowerCase().includes(query.toLowerCase()))
  return <div className="page fade-in">
    <SectionTitle eyebrow="SEU ESPAÇO DE TRABALHO" title="Meus projetos" description="Organize seus produtos, histórias e planejamentos em um só lugar." action={<Button onClick={()=>openEdit(null)}><Plus size={17}/> Novo projeto</Button>}/>
    <div className="projects-toolbar"><div className="search-input"><Search size={18}/><input aria-label="Buscar projetos" value={query} onChange={e=>setQuery(e.target.value)} placeholder="Buscar por nome ou descrição..."/></div><span>{items.length} projeto{items.length!==1?'s':''} no total</span></div>
    {loading?<div className="loading-state"><div className="spinner"/>Buscando projetos...</div>:error&&!items.length?<Message message={error}/>:filtered.length===0?<Empty title={query?'Nenhum resultado encontrado':'Seu primeiro projeto começa aqui'} description={query?'Tente outra palavra-chave.':'Crie um projeto para organizar os requisitos e montar o seu Product Backlog.'} action={!query?<Button onClick={()=>openEdit(null)}><Plus size={16}/> Criar meu projeto</Button>:undefined}/>:<div className="project-grid">{filtered.map((p,i)=><article key={p.id} className="project-card"><div className="project-card-top"><span className={`project-card-icon accent-${i%4}`}><FolderOpen size={23}/></span><span className="project-menu"><button className="icon-btn" title="Editar projeto" onClick={()=>openEdit(p)}><Pencil size={17}/></button><button className="icon-btn danger-icon" title="Excluir projeto" onClick={()=>setRemove(p)}><Trash2 size={17}/></button></span></div><h3>{p.nome}</h3><p>{p.descricao||'Projeto de software sem descrição. Você pode adicioná-la a qualquer momento.'}</p><div className="project-card-bottom"><span><CalendarDays size={15}/> {new Date(p.criado_em).toLocaleDateString('pt-BR')}</span><button className="open-project" onClick={()=>nav(`/projetos/${p.id}`)}>Abrir projeto <ArrowRight size={17}/></button></div></article>)}</div>}
    {edit!==undefined&&<Modal title={edit?'Editar projeto':'Criar novo projeto'} subtitle="Defina o contexto do produto de software que você vai gerenciar." onClose={()=>setEdit(undefined)}><form onSubmit={save} className="form-stack"><Field label="Nome do projeto" required><input value={nome} onChange={e=>setNome(e.target.value)} required maxLength={120} placeholder="Ex.: Sistema de gestão acadêmica" autoFocus/></Field><Field label="Descrição"><textarea value={descricao} onChange={e=>setDescricao(e.target.value)} rows={3} placeholder="Descreva brevemente o objetivo do projeto"/></Field><Message message={error}/><div className="modal-actions"><Button type="button" variant="outline" onClick={()=>setEdit(undefined)}>Cancelar</Button><Button loading={busy} type="submit">{edit?'Salvar alterações':'Criar projeto'} <ArrowRight size={16}/></Button></div></form></Modal>}
    {remove&&<Confirm title="Excluir projeto?" description={`Você está prestes a excluir "${remove.nome}". Todos os backlogs, épicos, histórias e critérios vinculados também serão removidos definitivamente. Essa ação não pode ser desfeita.`} onClose={()=>setRemove(null)} onConfirm={deleteIt} loading={busy}/>}
  </div>
}
