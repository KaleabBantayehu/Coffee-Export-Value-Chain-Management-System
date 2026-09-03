const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'
async function request(path, accessToken, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${accessToken}`, ...options.headers },
  })
  const body = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(body.detail ?? 'Farm request failed.')
  return body
}
export const createFarm = (body, token) => request('/farms', token, { method: 'POST', body: JSON.stringify(body) })
export const validateFarm = (id, token) => request(`/farms/${id}/validate`, token, { method: 'POST' })
