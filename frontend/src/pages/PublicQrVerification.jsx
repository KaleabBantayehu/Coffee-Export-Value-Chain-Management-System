import { useEffect, useState } from 'react'

import { verifyPublicQr } from '../api/verification'

const signaturePattern = /^[A-Za-z0-9_-]+$/
const approvedKeys = ['status', 'gin_code', 'origin_region', 'grade']

function isValidUrlInput(qrId, signature) {
  return /^[1-9]\d*$/.test(qrId) && signaturePattern.test(signature)
}

function isApprovedPublicResponse(payload) {
  if (!payload || typeof payload !== 'object') return false
  const keys = Object.keys(payload).sort()
  if (keys.length !== approvedKeys.length || !approvedKeys.every((key) => keys.includes(key))) return false
  return payload.status === 'valid'
    && typeof payload.gin_code === 'string'
    && (payload.origin_region === null || typeof payload.origin_region === 'string')
    && (payload.grade === null || typeof payload.grade === 'string')
}

export default function PublicQrVerification({ qrId }) {
  const [state, setState] = useState({ kind: 'loading', result: null })
  const signature = new URLSearchParams(window.location.search).get('sig') ?? ''
  const malformedUrl = !isValidUrlInput(qrId, signature)
  const displayState = malformedUrl ? { kind: 'invalid', result: null } : state

  useEffect(() => {
    if (malformedUrl) return undefined

    let active = true
    verifyPublicQr(qrId, signature)
      .then((result) => {
        if (!active) return
        setState(isApprovedPublicResponse(result)
          ? { kind: 'valid', result }
          : { kind: 'network', result: null })
      })
      .catch((error) => {
        if (!active) return
        if (error.status === 400) setState({ kind: 'invalid', result: null })
        else if (error.status === 404) setState({ kind: 'not-found', result: null })
        else setState({ kind: 'network', result: null })
      })

    return () => { active = false }
  }, [malformedUrl, qrId, signature])

  return (
    <section className="public-verification" aria-live="polite">
      <p className="eyebrow">CEVCMS PUBLIC VERIFICATION</p>
      {displayState.kind === 'loading' && <><h1>Checking QR code</h1><p>Please wait while we verify this QR code.</p></>}
      {displayState.kind === 'invalid' && <><h1>Invalid QR code</h1><p>This QR code cannot be verified.</p></>}
      {displayState.kind === 'not-found' && <><h1>QR code unavailable</h1><p>This QR code is not available for verification.</p></>}
      {displayState.kind === 'network' && <><h1>Verification unavailable</h1><p>We could not complete QR verification. Please try again later.</p></>}
      {displayState.kind === 'valid' && (
        <article className="verification-result">
          <h1>Verified coffee lot</h1>
          <p className="verification-status">Status: Valid</p>
          <dl>
            <div><dt>GIN code</dt><dd>{displayState.result.gin_code}</dd></div>
            <div><dt>Origin region</dt><dd>{displayState.result.origin_region ?? 'Not available'}</dd></div>
            {displayState.result.grade !== null && <div><dt>Grade</dt><dd>{displayState.result.grade}</dd></div>}
          </dl>
        </article>
      )}
    </section>
  )
}
