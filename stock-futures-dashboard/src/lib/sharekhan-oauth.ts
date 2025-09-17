import crypto from 'crypto'
import { cookies } from 'next/headers'

export function randomString(len = 43) {
  return crypto.randomBytes(len).toString('base64url')
}

export function setCookie(name: string, value: string, maxAgeSeconds = 3600) {
  cookies().set({ name, value, httpOnly: true, secure: false, sameSite: 'lax', path: '/', maxAge: maxAgeSeconds })
}

export function getCookie(name: string) {
  return cookies().get(name)?.value || null
}

export function clearCookie(name: string) {
  cookies().delete(name)
}

export function getOAuthConfig() {
  const clientId = process.env.SHAREKHAN_API_KEY || ''
  const clientSecret = process.env.SHAREKHAN_SECRET_KEY || ''
  const redirectUri = process.env.SHAREKHAN_REDIRECT_URI || ''
  const authBase = process.env.SHAREKHAN_AUTH_BASE || ''

  const authorizeUrl = `${authBase}/authorize`
  const tokenUrl = `${authBase}/token`

  return { clientId, clientSecret, redirectUri, authorizeUrl, tokenUrl }
}

