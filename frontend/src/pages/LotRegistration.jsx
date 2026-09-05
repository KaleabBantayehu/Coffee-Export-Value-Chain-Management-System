import { useEffect, useState } from 'react'

import { listFarms } from '../api/farms'
import { createLot } from '../api/lots'
import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'

export default function LotRegistration() {
  const { accessToken, role } = useAuth()
  const canRegister = role === 'Admin' || role === 'Field/Registry Agent'
  const [farms, setFarms] = useState([])
  const [farmId, setFarmId] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')
  const [createdLot, setCreatedLot] = useState(null)

  useEffect(() => {
    let cancelled = false

    const loadFarms = async () => {
      try {
        const result = await listFarms(accessToken)
        if (!cancelled) {
          setFarms(result)
          setError('')
        }
      } catch (requestError) {
        if (!cancelled) setError(requestError.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void loadFarms()
    return () => { cancelled = true }
  }, [accessToken])

  const submit = async (event) => {
    event.preventDefault()
    setCreatedLot(null)

    if (!farmId) {
      setError('Select a Farm before creating a Coffee Lot.')
      return
    }

    try {
      setSubmitting(true)
      setError('')
      const lot = await createLot(Number(farmId), accessToken)
      setCreatedLot(lot)
      setFarmId('')
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="farmer-page">
      <h1>Coffee Lot registration</h1>

      {!canRegister && <p>Lot registration is available to Admin and Field/Registry Agent roles.</p>}

      {canRegister && (
        <form className="login-form" onSubmit={submit}>
          <label htmlFor="farm-id">Existing Farm
            <select id="farm-id" value={farmId} onChange={(event) => setFarmId(event.target.value)} disabled={loading || submitting}>
              <option value="">{loading ? 'Loading Farms…' : 'Select a Farm'}</option>
              {farms.map((farm) => (
                <option key={farm.farm_id} value={farm.farm_id}>
                  Farm {farm.farm_id} — Farmer {farm.farmer_id} — {farm.area_hectares ?? 'Area unavailable'} ha
                </option>
              ))}
            </select>
          </label>

          {!loading && farms.length === 0 && <p>No Farms are available for Lot registration.</p>}
          <button disabled={loading || submitting || farms.length === 0}>
            {submitting ? 'Creating Coffee Lot…' : 'Create Coffee Lot'}
          </button>
        </form>
      )}

      {error && <p className="form-error" role="alert">{error}</p>}
      {createdLot && (
        <article className="session-status" aria-live="polite">
          <h2>Coffee Lot created</h2>
          <p>GIN: {createdLot.gin_code}</p>
          <p>Status: {createdLot.status}</p>
          {canRegister && (
            <button type="button" onClick={() => navigate(`/lots/${createdLot.lot_id}/qr`)}>
              Generate QR
            </button>
          )}
        </article>
      )}
    </section>
  )
}
