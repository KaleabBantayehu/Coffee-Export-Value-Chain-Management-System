const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

async function request(path, accessToken, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
      ...options.headers,
    },
  })
  const body = await response.json().catch(() => ({}))

  if (!response.ok) {
    throw new Error(body.detail ?? 'Unable to complete the lot request.')
  }

  return body
}

export const createLot = (farmId, accessToken) => request('/lots', accessToken, {
  method: 'POST',
  body: JSON.stringify({ farm_id: farmId }),
})

export const getLotTrace = (lotId, accessToken) => request(`/lots/${lotId}/trace`, accessToken)

export const appendTraceabilityEvent = (lotId, body, accessToken) => request(`/lots/${lotId}/events`, accessToken, {
  method: 'POST',
  body: JSON.stringify(body),
})

export const generateLotQr = (lotId, accessToken) => request(`/lots/${lotId}/qr`, accessToken, {
  method: 'POST',
  body: JSON.stringify({}),
})
