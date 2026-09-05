let sessionExpiryHandler = null

export function registerSessionExpiryHandler(handler) {
  sessionExpiryHandler = handler

  return () => {
    if (sessionExpiryHandler === handler) sessionExpiryHandler = null
  }
}

export function expireAuthenticatedSession() {
  sessionExpiryHandler?.()
}
