import { useMemo, useState } from 'react'

import { login } from '../api/auth'
import { AuthContext } from './authContext'

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null)
  const [role, setRole] = useState(null)

  const signIn = async (credentials) => {
    const response = await login(credentials)

    setAccessToken(response.access_token)
    setRole(response.role)

    return response
  }

  const value = useMemo(
    () => ({
      accessToken,
      role,
      isAuthenticated: Boolean(accessToken),
      signIn,
    }),
    [accessToken, role],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}