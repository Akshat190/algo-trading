import { NextResponse } from 'next/server'
import { getOAuthConfig, randomString, setCookie } from '../../../../lib/sharekhan-oauth'

// Starts the OAuth flow by redirecting to Sharekhan authorize
export async function GET() {
  const { clientId, redirectUri, authorizeUrl } = getOAuthConfig()

  if (!clientId || !redirectUri || !authorizeUrl) {
    return NextResponse.json({ error: 'Missing OAuth config. Check .env.local' }, { status: 500 })
  }

  // Basic state to prevent CSRF
  const state = randomString(16)
  setCookie('sk_oauth_state', state, 600)

  // You may need to adjust the query params to match Sharekhan docs
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'read write',
    state
  })

  const url = `${authorizeUrl}?${params.toString()}`
  return NextResponse.redirect(url)
}

