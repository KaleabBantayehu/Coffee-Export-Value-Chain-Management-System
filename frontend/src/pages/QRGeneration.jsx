import { useState } from 'react'

import { generateLotQr } from '../api/lots'
import { useAuth } from '../context/useAuth'

const allowedRoles = new Set(['Admin', 'Field/Registry Agent'])
const responseKeys = ['qr_id', 'verification_url', 'image_svg', 'image_png_data_url']

function isApprovedQrResponse(payload) {
  if (!payload || typeof payload !== 'object') return false
  const keys = Object.keys(payload).sort()
  if (keys.length !== responseKeys.length || !responseKeys.every((key) => keys.includes(key))) return false
  return Number.isInteger(payload.qr_id)
    && typeof payload.verification_url === 'string'
    && typeof payload.image_svg === 'string'
    && typeof payload.image_png_data_url === 'string'
    && payload.image_svg.startsWith('data:image/svg+xml;base64,')
    && payload.image_png_data_url.startsWith('data:image/png;base64,')
}

async function downloadPng(imageUrl, lotId) {
  const response = await fetch(imageUrl)
  if (!response.ok) throw new Error('Unable to prepare the QR download.')
  const objectUrl = URL.createObjectURL(await response.blob())
  const link = document.createElement('a')
  link.href = objectUrl
  link.download = `cevcm-lot-${lotId}-qr.png`
  document.body.appendChild(link)
  link.click()
  link.remove()
  URL.revokeObjectURL(objectUrl)
}

export default function QRGeneration({ lotId }) {
  const { accessToken, role } = useAuth()
  const [qr, setQr] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const generate = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await generateLotQr(lotId, accessToken)
      if (!isApprovedQrResponse(response)) {
        throw new Error('The QR response was not in the approved format.')
      }
      setQr(response)
    } catch (requestError) {
      setQr(null)
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }

  if (!allowedRoles.has(role)) {
    return (
      <section className="qr-page">
        <h1>QR generation</h1>
        <p className="form-error" role="alert">QR generation is available to Admin and Field/Registry Agent roles.</p>
      </section>
    )
  }

  return (
    <section className="qr-page">
      <h1>Generate QR</h1>
      <p>Generate the approved QR representation for Coffee Lot {lotId}.</p>
      <button type="button" onClick={generate} disabled={loading}>
        {loading ? 'Generating QR…' : qr ? 'Reuse active QR' : 'Generate QR'}
      </button>
      {error && <p className="form-error" role="alert">{error}</p>}
      {qr && (
        <article className="qr-result" aria-live="polite">
          <h2>QR generated</h2>
          <img src={qr.image_png_data_url} alt={`QR code for Coffee Lot ${lotId}`} />
          <p>QR ID: {qr.qr_id}</p>
          <p>
            Verification link:{' '}
            <a href={qr.verification_url} target="_blank" rel="noreferrer">
              {qr.verification_url}
            </a>
          </p>
          <div className="qr-actions">
            <button type="button" onClick={async () => {
              try {
                setError('')
                await downloadPng(qr.image_png_data_url, lotId)
              } catch (downloadError) {
                setError(downloadError.message)
              }
            }}>Download PNG</button>
            <button type="button" onClick={() => window.print()}>Print QR</button>
          </div>
        </article>
      )}
    </section>
  )
}
