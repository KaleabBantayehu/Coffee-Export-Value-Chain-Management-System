import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'
import { navigationByRole } from './navigationItems'

function Navigation() {
  const { role, signOut } = useAuth()
  const items = navigationByRole[role] ?? []

  const handleLogout = async () => {
    await signOut()
    navigate('/login')
  }

  return (
    <nav className="navigation" aria-label="Main navigation">
      <span className="role-label">{role}</span>
      {items.map((item) => <button key={item.path} type="button" onClick={() => navigate(item.path)}>{item.label}</button>)}
      <button type="button" className="logout-button" onClick={handleLogout}>Log out</button>
    </nav>
  )
}

export default Navigation
