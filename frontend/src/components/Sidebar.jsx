import { useLocation, Link } from 'react-router-dom'
import '../styles/components/_sidebar.scss'


const navItems = [
  { icon: 'ti-layout-dashboard', label: 'Dashboard', path: '/' },
  { icon: 'ti-cards', label: 'Mes mains', path: '/hands' },
  { icon: 'ti-alert-triangle', label: 'Leaks', path: '/leaks' },
  { icon: 'ti-users', label: 'Adversaires', path: '/opponents' },
  { icon: 'ti-target', label: 'Entraînement', path: '/training' },
  { icon: 'ti-medal', label: 'IQ Score', path: '/score' },
  { icon: 'ti-trending-up', label: 'Simulateur', path: '/simulator' },
  { icon: 'ti-star', label: 'Statut VIP', path: '/vip' },
  { icon: 'ti-file-text', label: 'Rapport IA', path: '/report' },
]

function Sidebar() {
  const location = useLocation()

  return (
    <aside className="sidebar">
      <div className="sidebar__logo">
        <div className="sidebar__logo-icon">IQ</div>
        <div>
          <p className="sidebar__logo-name">Grindset</p>
          <p className="sidebar__logo-sub">EXPRESSO · WINAMAX</p>
        </div>
      </div>
      <nav className="sidebar__nav">
        {navItems.map(item => (
          <Link
            key={item.path}
            to={item.path}
            className={`sidebar__item ${location.pathname === item.path ? 'active' : ''}`}
          >
            <i className={`ti ${item.icon}`} aria-hidden="true"></i>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  )
}

export default Sidebar