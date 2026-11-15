import React, {useEffect} from 'react'
import {AlertTriangle, Inbox, X, LoaderCircle} from 'lucide-react'

export function Button({children,variant='primary',size='',loading=false,...props}:React.ButtonHTMLAttributes<HTMLButtonElement>&{variant?:'primary'|'secondary'|'ghost'|'danger'|'outline';size?:string;loading?:boolean}){
  return <button {...props} className={`btn btn-${variant} ${size} ${props.className||''}`} disabled={props.disabled||loading}>{loading?<LoaderCircle size={16} className="spin"/>:null}{children}</button>
}
export function Field({label,required,children,hint}:{label:string;required?:boolean;children:React.ReactNode;hint?:string}){
  return <label className="field"><span className="label">{label}{required&&<span className="required"> *</span>}</span>{children}{hint&&<span className="field-hint">{hint}</span>}</label>
}
export function Modal({title,subtitle,children,onClose,wide=false}:{title:string;subtitle?:string;children:React.ReactNode;onClose:()=>void;wide?:boolean}){
  useEffect(()=>{const cb=(e:KeyboardEvent)=>{if(e.key==='Escape')onClose()};document.addEventListener('keydown',cb);return()=>document.removeEventListener('keydown',cb)},[onClose])
  return <div className="modal-backdrop" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}><section className={`modal ${wide?'modal-wide':''}`} role="dialog" aria-modal="true" aria-label={title}><header className="modal-header"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div><button className="icon-btn" type="button" aria-label="Fechar" onClick={onClose}><X size={19}/></button></header><div className="modal-content">{children}</div></section></div>
}
export function Confirm({title,description,confirmText='Excluir definitivamente',onConfirm,onClose,loading=false}:{title:string;description:string;confirmText?:string;onConfirm:()=>void;onClose:()=>void;loading?:boolean}){
  return <Modal title={title} onClose={onClose}><div className="warning-block"><AlertTriangle size={21}/><p>{description}</p></div><div className="modal-actions"><Button variant="outline" onClick={onClose} disabled={loading}>Cancelar</Button><Button variant="danger" onClick={onConfirm} loading={loading}>{confirmText}</Button></div></Modal>
}
export function Empty({title,description,action}:{title:string;description:string;action?:React.ReactNode}){
  return <div className="empty-panel"><div className="empty-icon"><Inbox size={27}/></div><h3>{title}</h3><p>{description}</p>{action}</div>
}
export function SectionTitle({eyebrow,title,description,action}:{eyebrow?:string;title:string;description?:string;action?:React.ReactNode}){
  return <div className="section-title"><div>{eyebrow&&<div className="eyebrow">{eyebrow}</div>}<h1>{title}</h1>{description&&<p>{description}</p>}</div>{action&&<div className="section-actions">{action}</div>}</div>
}
export function Priority({type}:{type:string|null}){
  const labels:Record<string,string>={M:'Must have',S:'Should have',C:'Could have',W:"Won't have"}
  return <span className={`priority priority-${type||'none'}`}>{type?`${type} · ${labels[type]}`:'Não definida'}</span>
}
export function StateChip({status}:{status:string}){
  const labels:Record<string,string>={A_FAZER:'A fazer',EM_ANDAMENTO:'Em andamento',CONCLUIDA:'Concluída'}
  return <span className={`state state-${status}`}>{labels[status]||status}</span>
}
export function Rice({score,state}:{score:string|null;state:string}){
  if(state==='CALCULADO')return <span className="rice-chip">{Number(score).toLocaleString('pt-BR',{minimumFractionDigits:2,maximumFractionDigits:2})}</span>
  return <span className="rice-muted">{state==='NAO_CALCULAVEL'?'Não calculável':'Pendente'}</span>
}
export function Message({message}:{message:string}){return message?<div className="form-error" role="alert">{message}</div>:null}
