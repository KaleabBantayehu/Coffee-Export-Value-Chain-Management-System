import { useEffect, useState } from 'react'
import { AuthProvider } from './context/AuthContext.jsx'
import { useAuth } from './context/useAuth'
import Navigation from './components/Navigation'
import { navigate } from './routes/navigate'
import Login from './pages/Login'
import ProtectedRoute from './routes/ProtectedRoute'
import Farmers from './pages/Farmers'
import FarmRegistration from './pages/FarmRegistration'
import LotRegistration from './pages/LotRegistration'
import LotTraceView from './pages/LotTraceView'
import QRGeneration from './pages/QRGeneration'
import PublicQrVerification from './pages/PublicQrVerification'
import './App.css'

const placeholderLabels = {
  '/users': 'User management',
  '/farmers': 'Farmer registration',
  '/farms': 'Farm registration',
  '/lots': 'Coffee Lot registration',
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

  const publicVerificationMatch = path.match(/^\/verify(?:\/([^/]*))?$/)
  const publicQrId = publicVerificationMatch ? publicVerificationMatch[1] ?? '' : null

  useEffect(() => {
    if (!isAuthenticated && path !== '/login' && publicQrId === null) {
      navigate('/login')
    }
  }, [isAuthenticated, path, publicQrId])

  if (path === '/login') {
    return <Login />
  }

  if (publicQrId !== null) return <PublicQrVerification key={`${publicQrId}${window.location.search}`} qrId={publicQrId} />

  if (path === '/farmers') return <ProtectedRoute><Navigation /><Farmers /></ProtectedRoute>
  if (path === '/farms') return <ProtectedRoute><Navigation /><FarmRegistration /></ProtectedRoute>
  if (path === '/lots') return <ProtectedRoute><Navigation /><LotRegistration /></ProtectedRoute>
  const traceMatch = path.match(/^\/lots\/(\d+)\/trace$/)
  if (traceMatch) return <ProtectedRoute><Navigation /><LotTraceView lotId={Number(traceMatch[1])} /></ProtectedRoute>
  const qrMatch = path.match(/^\/lots\/(\d+)\/qr$/)
  if (qrMatch) return <ProtectedRoute><Navigation /><QRGeneration lotId={Number(qrMatch[1])} /></ProtectedRoute>

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
