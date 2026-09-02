import { useEffect, useState } from 'react'
import { AuthProvider } from './context/AuthContext.jsx'
import { useAuth } from './context/useAuth'
import Navigation from './components/Navigation'
import { navigate } from './routes/navigate'
import Login from './pages/Login'
import ProtectedRoute from './routes/ProtectedRoute'
import Farmers from './pages/Farmers'
import './App.css'

const placeholderLabels = {
  '/users': 'User management',
  '/farmers': 'Farmer registration',
  '/farms': 'Farm registration',
  '/verification': 'QR verification',
}

function ApplicationShell() {
  const { isAuthenticated, role } = useAuth()
  const [path, setPath] = useState(window.location.pathname)

  useEffect(() => {
    const updatePath = () => setPath(window.location.pathname)

    window.addEventListener('popstate', updatePath)

    return () => window.removeEventListener('popstate', updatePath)
  }, [])

  useEffect(() => {
    if (isAuthenticated && path === '/login') {
      navigate('/dashboard')
    }
  }, [isAuthenticated, path])

  useEffect(() => {
    if (!isAuthenticated && path !== '/login') {
      navigate('/login')
    }
  }, [isAuthenticated, path])

  if (path === '/login') {
    return <Login />
  }

  if (path === '/farmers') return <ProtectedRoute><Navigation /><Farmers /></ProtectedRoute>

  const label = path === '/dashboard' ? 'Dashboard' : placeholderLabels[path]

  return (
    <ProtectedRoute>
      <Navigation />

      <section className="placeholder">
        <h1>{label ?? 'Page not found'}</h1>

        <p>
          {label
            ? `${label} is a placeholder. This screen will be implemented in its assigned epic.`
            : 'Choose an available navigation item.'}
        </p>

        <p className="session-status">
          Authenticated as {role}.
        </p>
      </section>
    </ProtectedRoute>
  )
}

function App() {
  return <AuthProvider><main className="app-shell"><section className="login-panel" aria-label="CEVCMS application"><p className="eyebrow">CEVCMS</p><ApplicationShell /></section></main></AuthProvider>
}

export default App
