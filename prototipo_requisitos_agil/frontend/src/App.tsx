import {Navigate, NavLink, Outlet, Route, Routes, useLocation, useNavigate} from 'react-router-dom'
import {BarChart3, Boxes, ChevronDown, ChevronRight, CircleHelp, LayoutDashboard, ListTodo, LogOut, Layers3, FolderKanban, Plus, ShieldCheck, Sparkles, Code2} from 'lucide-react'
import {useAuth, useProject, ProjectProvider} from './contexts'
import {Brand} from './components/Brand'
import {Button} from './components/ui'
import {LoginPage, RegisterPage} from './pages/Auth'
import {ProjectsPage} from './pages/Projects'
import {DashboardPage} from './pages/Dashboard'
import {BacklogPage} from './pages/Backlog'
import {SprintsPage} from './pages/Sprints'
import {EpicsPage} from './pages/Epics'
import {StoryEditorPage} from './pages/StoryEditor'
import {CriteriaPage} from './pages/Criteria'

function PrivateGate(){const {user,loading}=useAuth();if(loading)return <div className="full-loading"><div className="spinner"/>Preparando sua área de trabalho...</div>;return user?<Outlet/>:<Navigate to="/login" replace/>}
function PublicGate(){const {user,loading}=useAuth();if(loading)return <div className="full-loading"><div className="spinner"/></div>;return user?<Navigate to="/projetos" replace/>:<Outlet/>}
function AppShell(){
  const location=useLocation(); const nav=useNavigate(); const {user,logout}=useAuth();
  const match=location.pathname.match(/^\/projetos\/(\d+)/);const pid=match?Number(match[1]):null
  const projectBase=pid?`/projetos/${pid}`:''
  const links = pid ? [
    {to:projectBase,icon:<LayoutDashboard size={19}/>,title:'Visão geral',end:true},
    {to:`${projectBase}/backlog`,icon:<ListTodo size={19}/>,title:'Product Backlog'},
    {to:`${projectBase}/sprints`,icon:<FolderKanban size={19}/>,title:'Sprints'},
    {to:`${projectBase}/epicos`,icon:<Boxes size={19}/>,title:'Épicos'},
  ] : []
  return <div className="app-layout">
    <aside className="sidebar">
      <div className="sidebar-brand"><Brand dark/></div>
      <div className="sidebar-nav">
        <span className="nav-overline">ESPAÇO DE TRABALHO</span>
        <NavLink to="/projetos" className={({isActive})=>`side-link ${isActive&&!pid?'active':''}`}><LayoutDashboard size={19}/><span>Meus projetos</span></NavLink>
        {pid&&<><div className="nav-section-line"/><span className="nav-overline">PROJETO ATUAL</span>
          {links.map(x=><NavLink key={x.to} to={x.to} end={x.end} className={({isActive})=>`side-link ${isActive?'active':''}`}>{x.icon}<span>{x.title}</span></NavLink>)}</>}
      </div>
      <div className="sidebar-bottom">
        <div className="sidebar-helper"><div className="helper-head"><Sparkles size={17}/> Seu espaço, suas ideias</div><p>Transforme requisitos em entregas com clareza.</p></div>
        <div className="sidebar-profile"><span className="avatar">{user?.nome?.charAt(0).toUpperCase()}</span><span className="profile-meta"><strong>{user?.nome}</strong><small>{user?.email}</small></span><button title="Sair da conta" className="icon-btn logout-button" onClick={async()=>{await logout();nav('/login')}}><LogOut size={19}/></button></div>
      </div>
    </aside>
    <div className="main-wrap"><header className="topbar"><div className="mobile-brand"><Brand/></div><div className="topbar-path"><span>Workspace</span><ChevronRight size={15}/><strong>{pid?'Projeto':'Meus projetos'}</strong></div><div className="topbar-right"><span className="topbar-chip"><span className="live-dot"/> Ambiente acadêmico</span><span className="topbar-divider"/><span className="topbar-avatar">{user?.nome?.charAt(0).toUpperCase()}</span></div></header><main className="main-content"><Outlet/></main></div>
  </div>
}
function ProjectLayout(){
  const {project,pid}=useProject()
  const base=`/projetos/${pid}`
  return <>
    <div className="project-banner"><div><div className="eyebrow banner-eyebrow">PROJETO SELECIONADO</div><div className="banner-title-row"><span className="project-banner-icon"><FolderKanban size={24}/></span><div><h2>{project.nome}</h2><p>{project.descricao||'Planejamento e organização de requisitos de software'}</p></div></div></div><NavLink to="/projetos" className="banner-back">Trocar projeto <ChevronRight size={16}/></NavLink></div>
    <nav className="project-tabs" aria-label="Navegação do projeto"><NavLink end to={base}>Visão geral</NavLink><NavLink to={`${base}/backlog`}>Product Backlog</NavLink><NavLink to={`${base}/sprints`}>Sprint Backlogs</NavLink><NavLink to={`${base}/epicos`}>Épicos</NavLink></nav>
    <Outlet/>
  </>
}
export default function App(){return <Routes>
  <Route element={<PublicGate/>}><Route path="/login" element={<LoginPage/>}/><Route path="/cadastro" element={<RegisterPage/>}/></Route>
  <Route element={<PrivateGate/>}><Route element={<AppShell/>}>
    <Route index element={<Navigate to="/projetos" replace/>}/>
    <Route path="/projetos" element={<ProjectsPage/>}/>
    <Route path="/projetos/:pid" element={<ProjectProvider><ProjectLayout/></ProjectProvider>}>
      <Route index element={<DashboardPage/>}/>
      <Route path="backlog" element={<BacklogPage/>}/>
      <Route path="sprints" element={<SprintsPage/>}/>
      <Route path="epicos" element={<EpicsPage/>}/>
      <Route path="historias/nova" element={<StoryEditorPage/>}/>
      <Route path="historias/:stid" element={<StoryEditorPage/>}/>
      <Route path="historias/:stid/criterios" element={<CriteriaPage/>}/>
    </Route>
  </Route></Route>
  <Route path="*" element={<Navigate to="/projetos" replace/>}/>
</Routes>}
