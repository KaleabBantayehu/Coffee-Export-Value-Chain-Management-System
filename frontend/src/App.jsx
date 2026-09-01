import { AuthProvider } from './context/AuthContext.jsx'
import { useAuth } from "./context/useAuth";
import Login from './pages/Login'
import './App.css'

function SessionStatus() {
  const { role, isAuthenticated } = useAuth()
  return isAuthenticated ? <p className="session-status">Signed in as {role}.</p> : null
}

function App() {
  return <AuthProvider><main className="app-shell"><section className="login-panel" aria-labelledby="login-title"><p className="eyebrow">CEVCMS</p><h1 id="login-title">Sign in</h1><p className="intro">Coffee Export Value Chain Management System</p><Login /><SessionStatus /></section></main></AuthProvider>
}

export default App
