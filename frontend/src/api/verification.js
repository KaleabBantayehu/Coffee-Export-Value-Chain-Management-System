const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

export async function verifyPublicQr(qrId, signature) {
  const response = await fetch(
    `${API_BASE_URL}/verify/${encodeURIComponent(qrId)}?sig=${encodeURIComponent(signature)}`,
  )
  const body = await response.json().catch(() => ({}))

  if (!response.ok) {
    const error = new Error('Public QR verification was not successful.')
    error.status = response.status
    throw error
  }

  return body
}
