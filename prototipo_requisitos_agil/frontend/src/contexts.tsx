import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { Outlet, useParams } from 'react-router-dom'
import { api, ApiError } from './api'
import type { User, Project, Backlog, Sprint, Epic, Story } from './types'

type AuthContextType = { user:User|null; loading:boolean; login:(e:string,p:string)=>Promise<void>; register:(n:string,e:string,p:string)=>Promise<void>; logout:()=>Promise<void> }
const AuthContext = createContext<AuthContextType|null>(null)
export function useAuth(){ const ctx=useContext(AuthContext);if(!ctx)throw new Error('AuthProvider ausente');return ctx }
export function AuthProvider({children}:{children:React.ReactNode}){
  const [user,setUser]=useState<User|null>(null)
  const [loading,setLoading]=useState(true)
  useEffect(()=>{
    let active=true
    api.me().then(u=>{if(active)setUser(u)}).catch(()=>{if(active)setUser(null)}).finally(()=>{if(active)setLoading(false)})
    const unauth=()=>setUser(null)
    window.addEventListener('sr:unauthorized',unauth)
    return()=>{active=false;window.removeEventListener('sr:unauthorized',unauth)}
  },[])
  const login=async(e:string,p:string)=>setUser(await api.login(e,p))
  const register=async(n:string,e:string,p:string)=>{await api.register(n,e,p)}
  const logout=async()=>{await api.logout();setUser(null)}
  return <AuthContext.Provider value={{user,loading,login,register,logout}}>{children}</AuthContext.Provider>
}

type ToastContextType={push:(message:string,kind?:'success'|'error')=>void}
const ToastContext=createContext<ToastContextType|null>(null)
export function useToast(){const c=useContext(ToastContext);if(!c)throw new Error('ToastProvider ausente');return c}
export function ToastProvider({children}:{children:React.ReactNode}){
  const [toasts,setToasts]=useState<{id:number;msg:string;kind:'success'|'error'}[]>([])
  const push=(msg:string,kind:'success'|'error'='success')=>{
    const id=Date.now()+Math.random()
    setToasts(q=>[...q,{id,msg,kind}])
    window.setTimeout(()=>setToasts(q=>q.filter(t=>t.id!==id)),4200)
  }
  return <ToastContext.Provider value={{push}}>{children}<div className="toast-stack" aria-live="polite">{toasts.map(t=><div role="status" className={`toast toast-${t.kind}`} key={t.id}>{t.msg}<button aria-label="Dispensar" onClick={()=>setToasts(x=>x.filter(q=>q.id!==t.id))}>×</button></div>)}</div></ToastContext.Provider>
}

export type ProjectData = {pid:number; project:Project; backlog:Backlog|null; sprints:Sprint[]; epics:Epic[]; stories:Story[]; refresh:()=>Promise<void>}
const ProjectContext=createContext<ProjectData|null>(null)
export function useProject(){const c=useContext(ProjectContext);if(!c)throw new Error('Projeto não selecionado');return c}
export function ProjectProvider({children}:{children:React.ReactNode}){
  const params=useParams<{pid:string}>();const pid=Number(params.pid)
  const [project,setProject]=useState<Project|null>(null)
  const [backlog,setBacklog]=useState<Backlog|null>(null)
  const [sprints,setSprints]=useState<Sprint[]>([])
  const [epics,setEpics]=useState<Epic[]>([])
  const [stories,setStories]=useState<Story[]>([])
  const [error,setError]=useState('')
  const [loading,setLoading]=useState(true)
  const refresh=useCallback(async()=>{
    if(!pid||!Number.isFinite(pid))return
    const [p,b,s,e,h]=await Promise.all([api.project(pid),api.backlog(pid),api.sprints(pid),api.epics(pid),api.stories(pid)])
    setProject(p);setBacklog(b);setSprints(s);setEpics(e);setStories(h)
  },[pid])
  useEffect(()=>{
    setLoading(true);setError('')
    refresh().catch((e:ApiError)=>setError(e.message)).finally(()=>setLoading(false))
  },[refresh])
  if(loading)return <div className="loading-state"><div className="spinner"/>Carregando projeto...</div>
  if(error||!project)return <div className="page"><div className="empty-panel"><h2>Não foi possível abrir este projeto</h2><p>{error || 'Projeto não encontrado.'}</p></div></div>
  return <ProjectContext.Provider value={{pid,project,backlog,sprints,epics,stories,refresh}}>{children}</ProjectContext.Provider>
}
