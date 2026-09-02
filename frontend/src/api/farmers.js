const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

async function request(path, token, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', ...options.headers } })
  const payload = await response.json().catch(() => ({}))
  if (!response.ok) throw new Error(payload.detail ?? 'Unable to complete farmer request.')
  return payload
}

export const createFarmer = (body, token) => request('/farmers', token, { method: 'POST', body: JSON.stringify(body) })
export const searchFarmers = (search, token) => request(`/farmers${search ? `?search=${encodeURIComponent(search)}` : ''}`, token)
export const getFarmer = (id, token) => request(`/farmers/${id}`, token)
