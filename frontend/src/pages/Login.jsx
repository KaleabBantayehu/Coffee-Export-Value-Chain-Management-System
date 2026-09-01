import { useState } from 'react'
import { useAuth } from '../context/useAuth'
import { navigate } from '../routes/navigate'

function Login() {
  const { signIn } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await signIn({ username, password })
      setPassword('')
      navigate('/dashboard')
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsSubmitting(false)
    }
  }
  return <form className="login-form" onSubmit={handleSubmit}><label htmlFor="username">Username</label><input id="username" name="username" value={username} onChange={(event) => setUsername(event.target.value)} autoComplete="username" required /><label htmlFor="password">Password</label><input id="password" name="password" type="password" value={password} onChange={(event) => setPassword(event.target.value)} autoComplete="current-password" required />{error && <p className="form-error" role="alert">{error}</p>}<button type="submit" disabled={isSubmitting}>{isSubmitting ? 'Signing in…' : 'Sign in'}</button></form>
}

export default Login
