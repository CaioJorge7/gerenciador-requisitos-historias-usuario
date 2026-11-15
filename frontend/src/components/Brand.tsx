import {Layers3} from 'lucide-react'
export function Brand({dark=false}:{dark?:boolean}){
  return <div className={`brand ${dark?'brand-dark':''}`}><span className="brand-symbol"><Layers3 size={20} strokeWidth={2.6}/></span><span>requisito<span className="brand-dot">.</span></span></div>
}
