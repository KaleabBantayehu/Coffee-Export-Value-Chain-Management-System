import { useEffect, useMemo, useState } from 'react'

import { listFarms } from '../api/farms'
import { searchFarmers } from '../api/farmers'
import { navigationByRole } from '../components/navigationItems'
import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'

const initialCounts = {
  farmers: { state: 'loading' },
  farms: { state: 'loading' },
}

function controlledCountError(error) {
  if (error.message === 'You are not authorized to perform this action.') return error.message
  return 'Unable to load this dashboard count.'
}

function CountCard({ label, value }) {
  return (
    <article className="dashboard-card">
      <h2>{label}</h2>
      {value.state === 'loading' && <p>Loading {label.toLowerCase()}…</p>}
      {value.state === 'error' && <p className="form-error" role="alert">{value.message}</p>}
      {value.state === 'ready' && (
        value.count === 0
          ? <p>No registered {label.toLowerCase()}.</p>
          : <p className="dashboard-count">{value.count}</p>
      )}
    </article>
  )
}

export default function Dashboard() {
  const { accessToken, role } = useAuth()
  const [counts, setCounts] = useState(initialCounts)
  const actions = useMemo(
    () => (navigationByRole[role] ?? []).filter((item) => item.path !== '/dashboard'),
    [role],
  )

  useEffect(() => {
    let cancelled = false
    const load = (key, request) => {
      request()
        .then((items) => {
          if (!cancelled) setCounts((current) => ({ ...current, [key]: { state: 'ready', count: items.length } }))
        })
        .catch((error) => {
          if (!cancelled) setCounts((current) => ({ ...current, [key]: { state: 'error', message: controlledCountError(error) } }))
        })
    }

    load('farmers', () => searchFarmers('', accessToken))
    load('farms', () => listFarms(accessToken))

    return () => { cancelled = true }
  }, [accessToken])

  return (
    <section className="dashboard-page">
      <p className="eyebrow">AUTHENTICATED DASHBOARD</p>
      <h1>Dashboard</h1>
      <p className="intro">Choose an available action for your {role} role.</p>

      <div className="dashboard-counts" aria-label="Registered record counts">
        <CountCard label="Farmers" value={counts.farmers} />
        <CountCard label="Farms" value={counts.farms} />
      </div>

      <section className="dashboard-actions" aria-labelledby="dashboard-actions-heading">
        <h2 id="dashboard-actions-heading">Available actions</h2>
        <div>
          {actions.map((item) => (
            <button key={item.path} type="button" onClick={() => navigate(item.path)}>{item.label}</button>
          ))}
        </div>
      </section>
    </section>
  )
}
