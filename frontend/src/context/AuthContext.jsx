import { useCallback, useEffect, useMemo, useState } from 'react'

import { login, logout } from '../api/auth'
import { registerSessionExpiryHandler } from '../api/sessionExpiry'
import { navigate } from '../routes/navigate'
import { AuthContext } from './authContext'

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null)
  const [role, setRole] = useState(null)

  const signIn = useCallback(async (credentials) => {
    const response = await login(credentials)

    setAccessToken(response.access_token)
    setRole(response.role)

    return response
  }, [])

  const signOut = useCallback(async () => {
    try {
      if (accessToken) {
        await logout(accessToken)
      }
    } finally {
      setAccessToken(null)
      setRole(null)
    }
  }, [accessToken])

  const expireSession = useCallback(() => {
    setAccessToken(null)
    setRole(null)
    navigate('/login')
  }, [])

  useEffect(() => registerSessionExpiryHandler(expireSession), [expireSession])

  const value = useMemo(
    () => ({
      accessToken,
      role,
      isAuthenticated: Boolean(accessToken),
      signIn,
      signOut,
    }),
    [accessToken, role, signIn, signOut],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
