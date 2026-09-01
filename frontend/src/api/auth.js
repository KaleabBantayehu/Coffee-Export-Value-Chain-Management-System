const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

export async function login(credentials) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(credentials) })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(payload.detail ?? 'Unable to sign in. Please try again.')
  return payload
}

export async function logout(accessToken) {
  await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${accessToken}` },
  })
}
