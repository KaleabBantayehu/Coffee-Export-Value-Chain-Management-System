import { useEffect, useState } from 'react'

import { appendTraceabilityEvent, getLotTrace } from '../api/lots'
import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'

export default function LotTraceView({ lotId }) {
  const { accessToken, role } = useAuth()
  const canGenerateQr = role === 'Admin' || role === 'Field/Registry Agent'
  const [trace, setTrace] = useState(null)
  const [eventType, setEventType] = useState('')
  const [notes, setNotes] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    getLotTrace(lotId, accessToken)
      .then((result) => {
        if (!cancelled) {
          setTrace(result)
          setError('')
        }
      })
      .catch((requestError) => {
        if (!cancelled) {
          setTrace(null)
          setError(requestError.message)
        }
      })
      .finally(() => { if (!cancelled) setLoading(false) })

    return () => { cancelled = true }
  }, [accessToken, lotId])

  const submitEvent = async (event) => {
    event.preventDefault()
    if (!eventType.trim()) {
      setError('Enter an event type before appending an event.')
      return
    }

    try {
      setSubmitting(true)
      setError('')
      await appendTraceabilityEvent(lotId, { event_type: eventType.trim(), notes: notes || null }, accessToken)
      setEventType('')
      setNotes('')
      setTrace(await getLotTrace(lotId, accessToken))
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <section className="farmer-page"><h1>Traceability</h1><p>Loading traceability chain…</p></section>

  if (!trace) {
    return <section className="farmer-page"><h1>Traceability</h1><p className="form-error" role="alert">{error || 'Unable to load the traceability chain.'}</p></section>
  }

  return (
    <section className="farmer-page">
      <h1>Lot traceability</h1>
      <article>
        <h2>Lot</h2>
        <p>GIN: {trace.lot.gin_code}</p>
        <p>Status: {trace.lot.status}</p>
        <p>Created: {new Date(trace.lot.created_at).toLocaleString()}</p>
        {canGenerateQr && (
          <button type="button" onClick={() => navigate(`/lots/${lotId}/qr`)}>
            Generate QR
          </button>
        )}
      </article>
      <article>
        <h2>Originating Farm</h2>
        <p>Farm ID: {trace.farm.farm_id}</p>
        <p>Geometry: {trace.farm.geometry.type}</p>
        <p>Area: {trace.farm.area_hectares ?? 'Unavailable'} hectares</p>
        <p>Demonstration review flag: {String(trace.farm.eudr_risk_flag)}</p>
      </article>
      <article>
        <h2>Farmer</h2>
        <p>Name: {trace.farmer.full_name}</p>
        <p>FIN: {trace.farmer.fin_code}</p>
        <p>National ID: {trace.farmer.national_id}</p>
        <p>Phone: {trace.farmer.phone_number}</p>
      </article>
      <article>
        <h2>Traceability events</h2>
        {trace.events.length ? (
          <ol>
            {trace.events.map((item) => (
              <li key={item.event_id}>
                <strong>{item.event_type}</strong> — {new Date(item.event_timestamp).toLocaleString()}
                {item.notes && <span>: {item.notes}</span>}
              </li>
            ))}
          </ol>
        ) : <p>No events recorded.</p>}
      </article>
      <form className="login-form" onSubmit={submitEvent}>
        <h2>Append traceability event</h2>
        <label htmlFor="event-type">Event type
          <input id="event-type" value={eventType} onChange={(event) => setEventType(event.target.value)} required maxLength="128" />
        </label>
        <label htmlFor="event-notes">Notes (optional)
          <input id="event-notes" value={notes} onChange={(event) => setNotes(event.target.value)} />
        </label>
        <button disabled={submitting}>{submitting ? 'Appending event…' : 'Append event'}</button>
      </form>
      {error && <p className="form-error" role="alert">{error}</p>}
    </section>
  )
}
