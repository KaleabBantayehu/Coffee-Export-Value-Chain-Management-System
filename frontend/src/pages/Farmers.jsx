import { useEffect, useState } from 'react'
import { createFarmer, getFarmer, searchFarmers } from '../api/farmers'
import { useAuth } from '../context/useAuth'

const initial = { full_name: '', national_id: '', gender: '', phone_number: '', cooperative_id: '' }

export default function Farmers() {
  const { accessToken, role } = useAuth()
  const canRegister = role === 'Admin' || role === 'Field/Registry Agent'
  const [form, setForm] = useState(initial), [farmers, setFarmers] = useState([]), [selected, setSelected] = useState(null), [search, setSearch] = useState(''), [error, setError] = useState(''), [success, setSuccess] = useState(''), [loading, setLoading] = useState(true), [detailLoading, setDetailLoading] = useState(false)
  const load = async (term = '') => { try { setLoading(true); setError(''); setFarmers(await searchFarmers(term, accessToken)) } catch (err) { setError(err.message) } finally { setLoading(false) } }
  useEffect(() => {
    let cancelled = false
    searchFarmers('', accessToken)
      .then((result) => { if (!cancelled) setFarmers(result) })
      .catch((err) => { if (!cancelled) setError(err.message) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [accessToken])
  const submit = async (event) => { event.preventDefault(); if (Object.values(form).slice(0, 4).some((value) => !value.trim())) return setError('Complete all required fields.'); try { const payload = { ...form, cooperative_id: form.cooperative_id ? Number(form.cooperative_id) : null }; const farmer = await createFarmer(payload, accessToken); setSuccess(`Farmer registered. FIN: ${farmer.fin_code}`); setForm(initial); await load() } catch (err) { setError(err.message) } }
  const detail = async (id) => { try { setDetailLoading(true); setError(''); setSelected(await getFarmer(id, accessToken)) } catch (err) { setError(err.message) } finally { setDetailLoading(false) } }
  return <section className="farmer-page"><h1>Farmer registry</h1>{error && <p className="form-error">{error}</p>}{success && <p className="session-status">{success}</p>}{canRegister && <form className="login-form" onSubmit={submit}>{Object.entries(initial).map(([key]) => <label key={key}>{key.replaceAll('_', ' ')}{key === 'cooperative_id' ? <input value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} /> : <input required value={form[key]} onChange={(e) => setForm({ ...form, [key]: e.target.value })} />}</label>)}<button>Register farmer</button></form>}<label>Search <input value={search} onChange={(e) => { setSearch(e.target.value); load(e.target.value) }} /></label>{loading ? <p>Loading farmers…</p> : farmers.length ? <ul>{farmers.map((farmer) => <li key={farmer.farmer_id}><button onClick={() => detail(farmer.farmer_id)}>{farmer.full_name} — {farmer.fin_code}</button></li>)}</ul> : <p>No farmers found.</p>}{detailLoading && <p>Loading farmer details…</p>}{selected && <article><h2>{selected.full_name}</h2><p>FIN: {selected.fin_code}</p><p>National ID: {selected.national_id}</p><p>Phone: {selected.phone_number}</p><p>Linked farms: {selected.linked_farms.length}</p><p>Farms: {selected.farms.length}</p></article>}</section>
}
