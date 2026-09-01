import { useAuth } from '../context/useAuth'

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth()

  // Client routing is a UX guard only; FastAPI RBAC remains authoritative.
  if (!isAuthenticated) {
    return null
  }

  return children
}

export default ProtectedRoute