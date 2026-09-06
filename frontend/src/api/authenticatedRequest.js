import { expireAuthenticatedSession } from './sessionExpiry'

export function throwForProtectedRequest(response, body, fallbackMessage) {
  if (response.status === 401) {
    expireAuthenticatedSession()
    throw new Error('Your session has expired. Please sign in again.')
  }

  if (response.status === 403) {
    throw new Error('You are not authorized to perform this action.')
  }

  throw new Error(body.detail ?? fallbackMessage)
}
