const API_URL = import.meta.env.VITE_API_URL

export async function apiFetch(path: string, options: RequestInit = {}) {
  const token = localStorage.getItem('token')

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Something went wrong' }))
    throw new Error(error.detail ?? 'Request failed')
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}
