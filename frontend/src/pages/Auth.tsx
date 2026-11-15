import type React from 'react'
import {useState} from 'react'
import {ArrowRight, Check, ShieldCheck, Layers3, Sparkles, Zap} from 'lucide-react'
import {Link, useNavigate} from 'react-router-dom'
import {useAuth,useToast} from '../contexts'
import {Button,Field,Message} from '../components/ui'
import {Brand} from '../components/Brand'

function AuthFrame({children,heading,subheading}:{children:React.ReactNode;heading:string;subheading:string}){
  return <div className="auth-page"><div className="auth-form-pane"><div className="auth-brand"><Brand/></div><div className="auth-form-container"><div className="auth-kicker"><span className="kicker-dot"/> SUA PLATAFORMA DE REQUISITOS</div><h1>{heading}</h1><p className="auth-lede">{subheading}</p>{children}</div><div className="auth-foot">© 2026 Requisito. · Protótipo acadêmico de Engenharia de Software</div></div><div className="auth-art-pane"><div className="auth-glow glow-one"/><div className="auth-glow glow-two"/><div className="auth-art-inner"><span className="auth-art-tag"><Sparkles size={14}/> ORGANIZE O QUE IMPORTA</span><h2>Boas ideias merecem<br/><em>bons requisitos.</em></h2><p>Da primeira história ao planejamento de sprint. Tudo conectado, simples e em um só lugar.</p><div className="auth-preview"><div className="preview-top"><span className="preview-dots"><i/><i/><i/></span><span>Meu backlog</span><span className="preview-mini">Sprint 02</span></div><div className="preview-task"><span className="preview-check"><Check size={14}/></span><div><b>Como usuário, quero...</b><small>Autenticação segura no sistema</small></div><span className="preview-tag">Must</span></div><div className="preview-task"><span className="preview-check muted"><Layers3 size={14}/></span><div><b>Como analista, quero...</b><small>Priorizar requisitos por RICE</small></div><span className="preview-tag secondary">Should</span></div><div className="preview-stats"><span>24 <small>histórias</small></span><span>08 <small>épicos</small></span><span>3 <small>sprints</small></span></div></div></div><div className="auth-art-bottom"><ShieldCheck size={17}/> Planejamento ágil com regras de negócio verificáveis</div></div></div>
}
export function LoginPage(){
  const {login}=useAuth();const nav=useNavigate();const [email,setEmail]=useState('');const [senha,setSenha]=useState('');const [loading,setLoading]=useState(false);const [error,setError]=useState('')
  async function submit(e:React.FormEvent){e.preventDefault();setLoading(true);setError('');try{await login(email,senha);nav('/projetos')}catch(err:any){setError(err.message)}finally{setLoading(false)}}
  return <AuthFrame heading="Bem-vindo de volta." subheading="Entre na sua conta e continue transformando ideias em entregas."><form className="auth-form" onSubmit={submit}>
    <Field label="E-mail" required><input type="email" placeholder="seuemail@exemplo.com" value={email} onChange={e=>setEmail(e.target.value)} required autoComplete="email"/></Field>
    <Field label="Senha" required><input type="password" placeholder="Sua senha" minLength={8} value={senha} onChange={e=>setSenha(e.target.value)} required autoComplete="current-password"/></Field>
    <Message message={error}/><Button type="submit" loading={loading} className="auth-submit">Entrar na plataforma <ArrowRight size={18}/></Button>
  </form><div className="auth-alternative">Ainda não tem uma conta? <Link to="/cadastro">Criar conta gratuita</Link></div></AuthFrame>
}
export function RegisterPage(){
  const {register}=useAuth();const nav=useNavigate();const {push}=useToast();const [nome,setNome]=useState('');const [email,setEmail]=useState('');const [senha,setSenha]=useState('');const [loading,setLoading]=useState(false);const [error,setError]=useState('')
  async function submit(e:React.FormEvent){e.preventDefault();setError('');setLoading(true);try{await register(nome,email,senha);push('Conta criada com sucesso! Faça login para continuar.');nav('/login')}catch(err:any){setError(err.message)}finally{setLoading(false)}}
  return <AuthFrame heading="Comece por aqui." subheading="Crie sua conta para organizar projetos e histórias em um único espaço."><form className="auth-form" onSubmit={submit}>
    <Field label="Seu nome" required><input type="text" placeholder="Como podemos chamar você?" maxLength={100} value={nome} onChange={e=>setNome(e.target.value)} required autoComplete="name"/></Field>
    <Field label="E-mail" required><input type="email" placeholder="seuemail@exemplo.com" value={email} onChange={e=>setEmail(e.target.value)} required autoComplete="email"/></Field>
    <Field label="Crie uma senha" hint="Utilize pelo menos 8 caracteres." required><input type="password" placeholder="Pelo menos 8 caracteres" minLength={8} maxLength={128} value={senha} onChange={e=>setSenha(e.target.value)} required autoComplete="new-password"/></Field>
    <Message message={error}/><Button type="submit" loading={loading} className="auth-submit">Criar minha conta <ArrowRight size={18}/></Button>
  </form><div className="auth-alternative">Já possui uma conta? <Link to="/login">Fazer login</Link></div></AuthFrame>
}
