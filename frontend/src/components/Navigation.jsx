import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'

const navigationByRole = {
  Admin: [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/users', label: 'User management' },
  ],
  'ECTA Officer': [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/verification', label: 'QR verification' },
  ],
  'Field/Registry Agent': [
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/farmers', label: 'Farmer registration' },
    { path: '/farms', label: 'Farm registration' },
  ],
  Verifier: [],
}

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
