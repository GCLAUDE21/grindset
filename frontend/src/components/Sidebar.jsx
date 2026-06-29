import { Link, useLocation } from 'react-router-dom'
import Logo from './Logo'

const sections = [
  {
    label: 'Analyse',
    items: [
      { icon: 'ti-layout-dashboard', label: 'Dashboard', path: '/' },
      { icon: 'ti-cards', label: 'Mes sessions', path: '/sessions' },
      { icon: 'ti-alert-triangle', label: 'Leaks', path: '/leaks' },
      { icon: 'ti-users', label: 'Adversaires', path: '/opponents' },
    ]
  },
  {
    label: 'Progression',
    items: [
      { icon: 'ti-medal', label: 'IQ Score', path: '/score' },
      { icon: 'ti-target', label: 'Entraînement', path: '/training' },
      { icon: 'ti-flag', label: 'Objectifs', path: '/objectives' },
    ]
  },
  {
    label: 'Stratégie',
    items: [
      { icon: 'ti-cards', label: 'Ranges', path: '/ranges' },
      { icon: 'ti-trending-up', label: 'Simulateur', path: '/simulator' },
    ]
  },
  {
    label: 'Session',
    items: [
      { icon: 'ti-device-desktop', label: 'HUD', path: '/hud' },
    ]
  },
]

function Sidebar() {
  const location = useLocation()

  return (
    <aside className="sidebar">
      <div className="sidebar__logo">
        <Logo />
        <div>
          <p className="sidebar__logo-name">Grindset</p>
          <p className="sidebar__logo-sub">EXPRESSO · WINAMAX</p>
        </div>
      </div>

      <nav className="sidebar__nav">
        {sections.map(section => (
          <div key={section.label}>
            <p className="sidebar__section">{section.label}</p>
            {section.items.map(item => (
              <Link
                key={item.path}
                to={item.path}
                className={`sidebar__item ${location.pathname === item.path ? 'active' : ''}`}
              >
                <i className={`ti ${item.icon}`} aria-hidden="true"></i>
                <span>{item.label}</span>
              </Link>
            ))}
          </div>
        ))}
      </nav>

      <div className="sidebar__bottom">
        <Link to="/settings" className="sidebar__settings">
          <i className="ti ti-settings" aria-hidden="true"></i>
          <span>Paramètres</span>
        </Link>
      </div>
    </aside>
  )
}

export default Sidebar